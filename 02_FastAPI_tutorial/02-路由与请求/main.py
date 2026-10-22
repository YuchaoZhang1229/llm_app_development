"""
    路径参数、查询参数、枚举、列表
"""
from enum import Enum
from fastapi import FastAPI, Path, Query

app = FastAPI()

class TodoStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"

@app.get("/todos/{todo_id}")          # 路由声明：{todo_id} 是路径参数占位符
async def get_todo(
        todo_id: int = Path(..., ge=1),                # 路径参数，Path(...) 表示必填；ge=1 表示 ≥1，校验失败返回 422
        priority: int = Query(None, ge=1, le=5),       # 查询参数；Query约束，默认 None 即选填；ge/le 限定 1~5
        status: TodoStatus = Query(TodoStatus.pending, description="任务状态"),  # 枚举查询参数，默认 pending；取值只能是枚举成员，否则 422
        tags: list[str] = Query(None, description="标签列表，可重复传参"),          # 列表查询参数 list[str] 支持 ?tags=a&tags=b 重复传参；默认 None 表示选填
    ):
    return {"todo_id": todo_id, "priority": priority, "status": status, "tags": tags}  # 【重要】返回 dict，FastAPI 自动序列化（Enum 自动转字符串值）

# 【重要】调用示例：路径参数 + 查询参数 + 枚举 + 列表 混合传参
# http://localhost:8000/todos/6?priority=3
# http://localhost:8000/todos/6?priority=3&status=completed&tags=work&tags=urgent

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)  # 【重要】"main:app" 中的 main 必须与文件名 main.py 一致，否则启动失败