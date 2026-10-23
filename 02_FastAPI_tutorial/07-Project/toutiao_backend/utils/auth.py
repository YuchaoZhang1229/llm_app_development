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
