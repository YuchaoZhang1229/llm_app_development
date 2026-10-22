"""
路由系统
开发一个待办事项管理 API，包含：
- POST /todos — 创建待办（标题、描述、优先级）
- GET /todos — 列出所有待办（支持分页和按优先级筛选）
- GET /todos/{todo_id} — 获取单个待办
- PUT /todos/{todo_id} — 更新待办
- DELETE /todos/{todo_id} — 删除待办

数据校验
为待办事项 API 加上完善的数据校验：
- 定义 TodoCreate、TodoUpdate、TodoResponse 三个模型
- 标题长度限制 1-100 字符
- 优先级只能是 1-5 的整数
- 截止日期不能早于今天
- 使用 pydantic-settings 管理项目配置

依赖注入
为待办事项 API 添加：
- 统一的分页依赖
- 模拟用户登录依赖（返回固定用户信息）
- 需要登录才能创建/删除待办
- 不同用户只能操作自己的待办

安全与认证
为项目添加完整的认证系统：用户注册（密码哈希存储）、登录（JWT 签发）、获取当前用户、管理员权限控制。在 Swagger UI 中测试带认证的接口。

数据库集成
将待办事项 API 从内存存储迁移到 PostgreSQL（本地可用 SQLite 替代），实现完整的数据持久化。练习 Alembic 迁移、Repository 模式封装、数据库会话依赖注入。

中间件与工程化
重构待办事项 API：
- 采用分层项目结构
- 添加请求日志中间件
- 实现统一异常处理
- 配置 API 版本控制（`/api/v1/todos`）

"""


from fastapi import FastAPI, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from itertools import count
from datetime import datetime
from pydantic_model import TodoCreate, TodoUpdate, TodoResponse
from pydantic_setting import settings

app = FastAPI(title=settings.app_name)
# 允许跨域请求（解决浏览器调用时的 CORS 拦截问题）
(app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # 允许所有来源（学习阶段先放开，生产环境建议指定域名）
    allow_credentials=True,
    allow_methods=["*"],      # 允许所有 HTTP 方法
    allow_headers=["*"],      # 允许所有请求头
))

_id_seq = count(1)
todos_dict: dict[int, dict] = {}
# todos_dict: dict[int, dict] = {
#     1: {"title": "...", "description": "...", "priority": 1},
#     2: {"title": "...", "description": "...", "priority": 2},
# }

def _get_todo_or_404(todo_id: int) -> dict:
    todo = todos_dict.get(todo_id)
    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo {todo_id} not found",
        )
    return todo

# 创建待办（标题、描述、优先级、截止日期）
@app.post("/todos", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(todo_in: TodoCreate):
    todo_id = next(_id_seq)
    todo = {"todo_id": todo_id, **todo_in.model_dump(), "created_at": datetime.now(), "updated_at": None}
    todos_dict[todo_id] = todo
    return todo

# 获取所有待办（支持按优先级筛选）
@app.get("/todos", response_model=list[TodoResponse])
async def list_todos(priority: int | None = Query(None, ge=1, le=5, description= "按优先级筛选")):
    if priority is None:
        return list(todos_dict.values())
    else:
        return [todo for todo in todos_dict.values() if todo["priority"] == priority]  # List[dict]

# 获取单个待办
@app.get("/todos/{todo_id}", response_model=TodoResponse)    # 更新（全量）
async def get_todo(todo_id: int):
    return _get_todo_or_404(todo_id)

# 更新待办
@app.put("/todos/{todo_id}", response_model=TodoResponse)    # 更新（全量）
async def update_todos(todo_id: int, todo_in: TodoUpdate):
    todo = _get_todo_or_404(todo_id)
    todos_dict[todo_id] = {"todo_id": todo_id, **todo_in.model_dump(), "created_at": todo["created_at"], "updated_at": datetime.now()}
    return todos_dict[todo_id]

# 删除代办
@app.delete("/todos/{todo_id}") # 删除
async def delete_todos(todo_id: int):
    _get_todo_or_404(todo_id)
    del todos_dict[todo_id]
    return "删除成功"

# POST: http://localhost:8000/todos?title=router&priority=1

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("todos_project:app", host=settings.host, port=settings.port, reload=settings.reload)


"""
客户端请求 ──► FastAPI 路由层
                 │
                 ├─ 1. 路径/查询参数校验 (Path/Query)
                 │     └─ 类型错误/越界 ──► 自动返回 422
                 │
                 ├─ 2. 请求体校验 (Pydantic Model)
                 │     ├─ 基础约束 (min_length, ge, le) ──► 自动返回 422
                 │     └─ 自定义校验 (@field_validator) ──► 日期早于今天返回 422
                 │
                 └─ 3. 业务逻辑校验 (路由函数内)
                       └─ 字典 key 不存在 ──► 手动抛出 404
"""