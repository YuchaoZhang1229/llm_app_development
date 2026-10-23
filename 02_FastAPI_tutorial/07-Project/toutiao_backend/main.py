from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import users
from utils import exception
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # 允许访问的源
    allow_credentials=True,   # 允许携带 Cookie
    allow_methods=["*"],      # 允许所有 HTTP 请求方法
    allow_headers=["*"],      # 允许所有请求头
)

app.include_router(users.router)
exception.register_exception_handlers(app) # 注册全局异常处理

@app.get("/")
async def root():
    return {"message": "Hello World"}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)