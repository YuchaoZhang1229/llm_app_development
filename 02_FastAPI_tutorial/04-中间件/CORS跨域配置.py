"""
跨域资源共享（CORS）
同源策略三个条件：协议、域名、端口，三者缺一即为跨域
"""
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 允许发送请求的源
    allow_credentials=True, # 允许发送Cookie
    allow_methods=["*"],    # 允许所有HTTP方法
    allow_headers=["*"],    # 允许所有HTTP头
)