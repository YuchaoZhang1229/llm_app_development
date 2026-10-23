from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_conf import get_db
from schemas.users import UserRequest, UserAuthResponse, UserInfoResponse
from crud import users as user_crud
from utils.response import success_response
from utils.security import verify_password

# 接口实现流程
# 1. 模块化路由 → API接口规范文档
# 2. 定义模型类 → 数据库表 (数据库设计文档)
# 3. 在 crud 文件夹里面创建文件，封装操作数据库的方法
# 4. 在路由处理函数里面调用 crud 封装好的方法，响应结果

router = APIRouter(prefix="/api/user", tags=["users"])

# 用户注册
@router.post("/register")
async def user_register(user_data: UserRequest, db: AsyncSession = Depends(get_db)):
    # 用户注册逻辑：验证用户是否存在 -> 创建用户 -> 生成 Token -> 响应结果（token+user_info）
    # 1. 验证用户是否存在，存在报错， 否则创建用户
    existing_user = await user_crud.get_user_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户已经存在")
    # 2. 创建用户
    new_created_user = await user_crud.create_user(db, user_data)
    # 3. 生成 Token
    token = await  user_crud.create_token(db, new_created_user.id)
    # 4. 响应结果（token+user_info）
    response_data = UserAuthResponse(token=token, userInfo=UserInfoResponse.model_validate(new_created_user))
    return success_response(message="用户注册成功", data=response_data)

# 用户登录
@router.post("/login")
async def user_login(user_data: UserRequest, db: AsyncSession = Depends(get_db)):
    # 用户登录逻辑：验证用户是否存在和验证密码 -> 生成 Token -> 响应结果（token+user_info）
    existing_user = await user_crud.get_user_by_username(db, user_data.username)
    if existing_user and verify_password(user_data.password, existing_user.password):
        token = await user_crud.create_token(db, existing_user.id)
        response_data = UserAuthResponse(token=token, userInfo=UserInfoResponse.model_validate(existing_user))
        return success_response(message="用户登录成功", data=response_data)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")

# 获取用户信息
@router.get("/info")
async def get_user_info():
    return success_response(message="获取用户信息成功", data=None)

# 更新用户信息
@router.put("/update")
async def update_user_info():
    return success_response(message="更新用户信息成功", data=None)

# 修改用户密码
@router.put("/password")
async def update_user_password():
    return success_response(message="修改用户密码", data=None)