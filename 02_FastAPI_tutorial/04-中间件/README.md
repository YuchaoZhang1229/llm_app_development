## FastAPI 常用中间件速查表
| 中间件 | 典型用途 | 使用方式 |
|---|---|---|
| `CORSMiddleware` | 解决前后端跨域 | `app.add_middleware(CORSMiddleware, allow_origins=[...])` |
| `GZipMiddleware` | 压缩响应体，降低带宽 | `app.add_middleware(GZipMiddleware, minimum_size=1000)` |
| `HTTPSRedirectMiddleware` | HTTP 自动跳转 HTTPS | `app.add_middleware(HTTPSRedirectMiddleware)` |
| `TrustedHostMiddleware` | 校验 Host 头，防主机头攻击 | `app.add_middleware(TrustedHostMiddleware, allowed_hosts=[...])` |
| 请求日志中间件 | 记录方法、路径、状态码、耗时 | `@app.middleware("http")` 或 `BaseHTTPMiddleware` |
| 耗时统计中间件 | 监控接口性能 | 在 `call_next` 前后计时并写入响应头 |
| 全局错误处理中间件 | 统一异常格式、隐藏敏感信息 | 自定义 ASGI 中间件，或用 `@app.exception_handler` |
| 自定义头 / 请求 ID 中间件 | 链路追踪、调试、审计 | 从请求头取 ID，或生成后写入响应头 |



