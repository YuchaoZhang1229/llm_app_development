'''
开发一个待办事项管理 API，包含：
- POST /todos — 创建待办（标题、描述、优先级）
- GET /todos — 列出所有待办（支持分页和按优先级筛选）
- GET /todos/{todo_id} — 获取单个待办
- PUT /todos/{todo_id} — 更新待办
- DELETE /todos/{todo_id} — 删除待办
先用内存列表模拟数据库，重点关注路由定义、参数校验和响应模型。
'''

from fastapi import FastAPI, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from itertools import count

app = FastAPI()
# 允许跨域请求（解决 Apifox/浏览器调用时的 CORS 拦截问题）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # 允许所有来源（学习阶段先放开，生产环境建议指定域名）
    allow_credentials=True,
    allow_methods=["*"],      # 允许所有 HTTP 方法
    allow_headers=["*"],      # 允许所有请求头
)

_id_seq = count(1)
todos_dict: dict[int, dict] = {}
# todos_dict: dict[int, dict] = {
#     1: {"title": "...", "description": "...", "priority": 1},
#     2: {"title": "...", "description": "...", "priority": 2},
# }

class TodoResponse(BaseModel):
    title: str
    description: str | None = None
    priority: int

def _get_or_404(todo_id: int) -> dict:
    todo = todos_dict.get(todo_id)
    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo {todo_id} not found",
        )
    return todo

# 创建待办（标题、描述、优先级）
@app.post("/todos")
async def create_todo(title: str, priority: int = Query(..., ge=1, le=5), description: str | None = None):
    todo_id = next(_id_seq)
    todo = {"id": todo_id, "title": title, "priority": priority, "description": description}
    todos_dict[todo_id] = todo
    return todo

# 获取所有待办（支持按优先级筛选）
@app.get("/todos")          # 查询
async def list_todos(priority: int | None = None):
    if priority is None:
        return list(todos_dict.values())
    else:
        return [todo for todo in todos_dict.values() if todo["priority"] == priority]  # List[dict]

# 获取单个待办
@app.get("/todos/{todo_id}")    # 更新（全量）
async def get_todo(todo_id: int):
    _get_or_404(todo_id)
    return todos_dict[todo_id]

# 更新待办
@app.put("/todos/{todo_id}")    # 更新（全量）
async def update_todos(todo_id: int, title: str, priority: int, description: str | None = None):
    _get_or_404(todo_id)
    todos_dict[todo_id] = {"id": todo_id, "title": title, "priority": priority, "description": description}
    return todos_dict[todo_id]

# 删除代办
@app.delete("/todos/{todo_id}") # 删除
async def delete_todos(todo_id: int):
    _get_or_404(todo_id)
    del todos_dict[todo_id]
    return "删除成功"

# POST: http://localhost:8000/todos?title=router&priority=1

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("todos_project:app", host="127.0.0.1", port=8000, reload=True)