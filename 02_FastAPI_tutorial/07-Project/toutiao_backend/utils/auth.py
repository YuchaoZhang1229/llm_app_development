"""
用户认证 + 获取当前用户
"""
from fastapi import Header, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_conf import get_db
from crud import users as users_crud

# 获取 token -> 根据 token 获取用户
async def get_current_user(
        authorization: str = Header(..., alias="Authorization"),
        db: AsyncSession = Depends(get_db)
):
    # Bearer xxxxx
    # 1. 获取 token
    token = authorization.replace("Bearer ", "") # token = authorization.split(" ")[1]
    # 2. 根据 token 获取用户
    user = await users_crud.get_user_by_token(db, token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="无效的令牌或已经过期的令牌")
    return user

"""
密码加密与验证
"""

from passlib.context import CryptContext

# 创建加密上下问
pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")
# 加密
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
# 密码校验
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


if __name__ == "__main__":
    hashed_password = get_password_hash("123456xxx")
    res = verify_password("123456xxx", hashed_password)
    print(res)
