from fastapi import FastAPI

# 创建FastAPI应用实例
app = FastAPI()

# http://localhost:8000/
@app.get("/")
async def root():
    return {"message": "Hello, FastAPI!"}

# http://localhost:8000/items/100?q1=Hello
# http://localhost:8000/items/100?q1=Hello&q2=FastAPI
@app.get("/items/{item_id}")
async def read_item(item_id: int, q1: str, q2: str | None = None):
    return {"item_id": item_id, "q1": q1, "q2": q2}