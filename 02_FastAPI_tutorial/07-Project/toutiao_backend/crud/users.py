import uuid
from datetime import timedelta, datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from models.users import User, UserToken
from schemas.users import UserRequest, UserUpdateRequest
from utils import auth


# 根据 username 查询用户
async def get_user_by_username(db: AsyncSession, username: str):
    query = select(User).where(User.username == username)
    result = await db.execute(query)
    return  result.scalar_one_or_none()

# 创建用户
async def create_user(db: AsyncSession, user_data: UserRequest):
    # 密码加密处理 -> 存入数据库 user
    hashed_password = auth.get_password_hash(user_data.password)
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

# 根据 id 查询用户
async def get_user_by_id(db: AsyncSession, user_id):
    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    return  result.scalar_one_or_none()

# 根据 Token 查询用户：查询 Token -> 验证 Token 是否过期 -> 查询用户 -> 返回用户信息
async def get_user_by_token(db: AsyncSession, token: str):
    # 1. 查询 Token
    query = select(UserToken).where(UserToken.token == token)
    result = await db.execute(query)
    user_token = result.scalar_one_or_none()
    # 2. 验证 Token 是否过期
    if user_token and user_token.expires_at > datetime.now():
        return await get_user_by_id(db, user_token.user_id)
    else:
        return None

# 更新用户信息
async def update_user(db: AsyncSession, username: str, user_data: UserUpdateRequest):
    # model_dump: Pydantic -> dict
    update_data = user_data.model_dump(exclude_unset=True, exclude_none=True) # 字段没传或None的值不更新

    # 先确认用户存在，避免依赖 rowcount 的不可靠行为
    user = await get_user_by_username(db, username)
    if user is None:
        return None
    if not update_data:
        return user

    # **dict：dict -> 字段=值, 字段=值, ...
    query = update(User).where(User.username == username).values(**update_data)
    await db.execute(query)
    await db.commit()
    await db.refresh(user)
    return user

# 更新用户密码
async def update_password(db: AsyncSession, username: str, password: str):
    # 先确认用户存在，避免依赖 rowcount 的不可靠行为
    user = await get_user_by_username(db, username)
    if user is None:
        return None

    # 加密新密码
    hashed_password = auth.get_password_hash(password)
    # 更新密码
    query = update(User).where(User.username == username).values(password=hashed_password)
    await db.execute(query)
    await db.commit()
    await db.refresh(user)
    return user

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



