"""
（标题、描述、优先级、截止日期）
为待办事项 API 加上完善的数据校验：
- 定义 TodoCreate、TodoUpdate、TodoResponse 三个模型
- 标题长度限制 1-100 字符
- 描述长度限制 1-500 字符
- 优先级只能是 1-5 的整数
- 截止日期不能早于今天
- 使用 pydantic-settings 管理项目配置
"""

from pydantic import BaseModel, Field, field_validator
from datetime import date, datetime

class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="标题, 1-100字符")
    description: str | None = Field(None, min_length=1, max_length=500, description="描述, 1-500字符")
    priority: int = Field(..., ge=1, le=5, description="优先级, 1-5整数")
    due_date: date | None = Field(None, description="截止日期")

    @field_validator("due_date")
    @classmethod
    def check_due_date(cls, v: date | None) -> date | None:
        if v and v < date.today():
            raise ValueError("截止日期不能早于今天")
        return v

class TodoUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=100)
    description: str | None = Field(None, min_length=1, max_length=500)
    priority: int | None = Field(None, ge=1, le=5)
    due_date: date | None = None

    @field_validator("due_date")
    @classmethod
    def check_due_date(cls, v: date | None) -> date | None:
        if v is not None and v < date.today():
            raise ValueError("截止日期不能早于今天")
        return v

class TodoResponse(BaseModel):
    todo_id: int
    title: str
    description: str | None
    priority: int
    due_date: date | None
    created_at: datetime | None
    updated_at: datetime | None

    model_config = {"from_attributes": True}