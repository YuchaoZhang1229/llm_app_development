from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
class Gender(str, Enum):
    male = "male"
    female = "female"
    unknown = "unknown"

class UserRequest(BaseModel):
    username: str = Field(..., max_length=50, description="用户名")
    password: str = Field(..., max_length=255, description = "登录密码")  # SecretStr

class UserUpdateRequest(BaseModel):
    nickname: str | None = Field(None, max_length=50, description="昵称")
    avatar: str | None = Field(None, max_length=255, description="头像URL")
    gender:  Gender | None = Field(None, max_length=10, description="性别")
    bio: str | None = Field(None, max_length=500, description="个人简介")
    phone: str | None = Field(None, max_length=20, description="手机号")

    model_config = ConfigDict(
        from_attributes=True,  # 允许从 ORM 对象属性中取值
    )

class UserInfoResponse(BaseModel):
    id: int
    username: str = Field(..., max_length=50, description="用户名")
    nickname: str | None = Field(None, max_length=50, description="昵称")
    avatar: str | None = Field(None, max_length=255, description="头像URL")
    gender:  Gender | None = Field(None, max_length=10, description="性别")
    bio: str | None = Field(None, max_length=500, description="个人简介")
    phone: str | None = Field(None, max_length=20, description="手机号")

    model_config = ConfigDict(
        from_attributes=True,  # 允许从 ORM 对象属性中取值
    )

class UserAuthResponse(BaseModel):
    token: str = Field(..., max_length=255, description="访问令牌")
    user_info: UserInfoResponse = Field(..., alias="userInfo")
    model_config = ConfigDict(
        from_attributes=True,  # 允许从 ORM 对象属性中取值
        populate_by_name=True, # 别名兼容
    )