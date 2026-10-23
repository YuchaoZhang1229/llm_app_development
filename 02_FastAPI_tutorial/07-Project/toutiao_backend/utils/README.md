## passlib 密码加密（security.py）
安装
```bash
uv add passlib[bcrypt] passlib[argon2] 
```

```python
from passlib.context import CryptContext
# 创建加密上下问
pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")
# 加密
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
# 密码校验
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
```

## 全局异常处理器（exception.py）
- 注册在 FastAPI 应用级别的`异常处理函数`
- 用于捕获业务层、数据层以及系统层抛出的异常
- 以`统一的响应格式`返回给前端

异常：
- SQL 错误
- 外键关联失败
- 数据库连接异常
- 提交事务失败

步骤
1. 定义异常处理器（函数）
2. 全局注册异常处理器 `app.add_exception_handle()`
