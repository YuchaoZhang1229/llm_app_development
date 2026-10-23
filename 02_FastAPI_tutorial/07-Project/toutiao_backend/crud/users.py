import uuid
from datetime import timedelta, datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.users import User, UserToken
from schemas.users import UserRequest
from utils import security


# 根据用户名查询数据库
async def get_user_by_username(db: AsyncSession, username: str):
    query = select(User).where(User.username == username)
    result = await db.execute(query)
    return  result.scalar_one_or_none()

# 创建用户
async def create_user(db: AsyncSession, user_data: UserRequest):
    # 密码加密处理 -> 存入数据库 user
    hashed_password = security.get_password_hash(user_data.password)
    user = User(username=user_data.username, password=hashed_password)
    db.add(user)
    await db.commit()
    await  db.refresh(user)
    return user

# 生成 Token
async def create_token(db: AsyncSession, user_id: int):
    # 生成 Token + 设置过期时间 -> 查询 user_token 数据库是否已存在该用户 -> 有：更新; 没有：存入 user_token 数据库
    token = str(uuid.uuid4())
    expires_at = datetime.now() + timedelta(days=7)

    query = select(UserToken).where(UserToken.user_id == user_id)
    result = await db.execute(query)
    user_token = result.scalar_one_or_none()

    if user_token:
        user_token.token = token
        user_token.expires_at = expires_at
    else:
        user_token = UserToken(user_id=user_id, token=token, expires_at=expires_at)
        db.add(user_token)
        await db.commit()
    return token


if __name__ == "__main__":
    import asyncio
    from config.db_conf import get_db, async_engine

    async def main():
        agen = get_db()
        session: AsyncSession = await anext(agen)  # 进入生成器，拿到 session
        try:
            res = await get_user_by_username(session, "admin")
            print(res)
        finally:
            await agen.aclose()  # 关闭生成器，等价于 async with 退出
            await async_engine.dispose()


    asyncio.run(main())



