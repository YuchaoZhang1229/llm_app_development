from datetime import datetime, timedelta, timezone
from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, status, Security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from passlib.context import CryptContext
from pydantic import BaseModel


# ---------- 配置 ----------
SECRET_KEY = "cd507226224ad25bfdf8e902b33e98fcd02443c56c81e240b28acb59dc4415b3"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# ---------- 密码与 JWT ----------
pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# ---------- 模型 ----------
class User(BaseModel):
    username: str
    role: str
    permissions: List[str]

class Token(BaseModel):
    access_token: str
    token_type: str

# ---------- 模拟数据 ----------
fake_users_db = {
    "admin": {
        "username": "admin",
        "hashed_password": pwd_context.hash("admin123"),
        "role": "admin",
        "permissions": ["task:create", "task:read", "task:update", "task:delete"],
    },
    "editor": {
        "username": "editor",
        "hashed_password": pwd_context.hash("editor123"),
        "role": "editor",
        "permissions": ["task:create", "task:read", "task:update"],
    },
    "viewer": {
        "username": "viewer",
        "hashed_password": pwd_context.hash("viewer123"),
        "role": "viewer",
        "permissions": ["task:read"],
    },
}

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# ---------- 认证依赖 ----------
def get_current_user(token: str = Security(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无效的认证凭证",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: Optional[str] = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.exceptions:
        raise credentials_exception

    user_dict = fake_users_db.get(username)
    if user_dict is None:
        raise credentials_exception

    return User(
        username=user_dict["username"],
        role=user_dict["role"],
        permissions=user_dict["permissions"],
    )

# ---------- RBAC 依赖 ----------
def require_roles(*allowed_roles: str):
    def checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="角色权限不足",
            )
        return current_user
    return checker

def require_permissions(*required_perms: str, require_all: bool = True):
    def checker(current_user: User = Depends(get_current_user)):
        user_perms = set(current_user.permissions)
        if require_all:
            if not set(required_perms).issubset(user_perms):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="缺少必要权限",
                )
        else:
            if not set(required_perms) & user_perms:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="缺少必要权限",
                )
        return current_user
    return checker

# ---------- 接口 ----------
app = FastAPI()

@app.post("/auth/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Security()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict or not verify_password(form_data.password, user_dict["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={
            "sub": user_dict["username"],
            "role": user_dict["role"],
            "permissions": user_dict["permissions"],
        }
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/tasks")
def list_tasks(user: User = Depends(require_permissions("task:read"))):
    return {"user": user.username, "role": user.role, "tasks": []}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, user: User = Depends(require_roles("admin"))):
    return {"deleted": task_id, "operator": user.username}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("jwt认证:app", host="127.0.0.2", port=8000, reload=True)