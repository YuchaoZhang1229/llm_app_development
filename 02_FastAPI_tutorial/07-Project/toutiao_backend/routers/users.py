from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_conf import get_db
from models.users import User
from schemas.users import UserRequest, UserUpdateRequest, UserAuthResponse, UserInfoResponse
from crud import users as user_crud
from utils.response import success_response
from utils.security import verify_password
from utils.auth import get_current_user

# 接口实现流程
# 1. 模块化路由 → API接口规范文档
# 2. 定义模型类 → 数据库表 (数据库设计文档)
# 3. 在 crud 文件夹里面创建文件，封装操作数据库的方法
# 4. 在路由处理函数里面调用 crud 封装好的方法，响应结果

router = APIRouter(prefix="/api/user", tags=["users"])

# 用户注册
@router.post("/register")
async def user_register(user_data: UserRequest, db: AsyncSession = Depends(get_db)):
    # 用户注册逻辑：通过 username 验证用户是否存在 -> 创建用户 -> 生成 Token -> 响应结果（token+user_info）
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
    # 用户登录逻辑：通过 username 验证用户是否存在并验证密码 -> 生成 Token -> 响应结果（token+user_info）
    existing_user = await user_crud.get_user_by_username(db, user_data.username)
    if existing_user and verify_password(user_data.password, existing_user.password):
        token = await user_crud.create_token(db, existing_user.id)
        response_data = UserAuthResponse(token=token, userInfo=UserInfoResponse.model_validate(existing_user))
        return success_response(message="用户登录成功", data=response_data)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")

# 获取用户信息
@router.get("/info")
async def get_user_info(user: User = Depends(get_current_user)):
    # 获取用户信息逻辑：根据 Token 查询用户 (检查 Token 是否过期，查询对应用户) -> 依赖注入方式导入路由
    return success_response(message="获取用户信息成功", data=UserInfoResponse.model_validate(user))

# 更新用户信息
@router.put("/update")
async def update_user_info(user_data: UserUpdateRequest, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    # 更新用户信息逻辑：根据 username 更新用户信息 -> 检查是否命中 -> 获取更新后的用户 -> 响应结果
    user = await user_crud.update_user(db, user.username, user_data)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")
    return success_response(message="更新用户信息成功", data=UserInfoResponse.model_validate(user))

# 修改用户密码
@router.put("/password")
async def update_user_password(user: User= Depends(get_current_user)):
    return success_response(message="密码修改成功", data=None)