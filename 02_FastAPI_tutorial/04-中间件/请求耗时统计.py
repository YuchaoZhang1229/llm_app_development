"""
请求耗时统计中间件
"""
import time
from fastapi import Request, FastAPI, Response
app = FastAPI()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request) # 调用下一个中间件或路由处理函数
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time) # 全局添加响应头
    return response

@app.get("/")
async def add_response_header(response: Response):
    response.headers["X"] = "value" # 添加响应头
    return {"Hello": "World", "Response": response.headers}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("请求耗时统计:app", host="127.0.0.2", port=8000, reload=True)
