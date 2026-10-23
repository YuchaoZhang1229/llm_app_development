
## FastAPI 协作全景图
现在回过头来看整个系统的请求处理流程：
```
客户端请求
    ↓
[中间件层 - 第二章]
    ├── CORS 中间件：检查跨域
    ├── 日志中间件：记录请求
    └── 耗时中间件：开始计时
    ↓
[依赖注入层 - 第一章 + 第三章]
    ├── oauth2_scheme：提取 Token
    ├── get_current_user：解析 Token → 查数据库（第四章）
    ├── get_current_active_user：检查用户状态
    └── require_role：检查角色权限
    ↓
[路由函数]
    ├── get_db：创建数据库会话（第四章的 yield 依赖）
    ├── pagination_params：解析分页参数（第一章的泛型依赖）
    └── 执行业务逻辑（CRUD 操作）
    ↓
[中间件层 - 后置]
    ├── 耗时中间件：计算耗时，写入响应头
    └── 日志中间件：记录响应状态
    ↓
返回响应给客户端
```
> 中间件做全局管控，依赖注入做参数传递和权限校验，认证系统识别用户身份，数据库负责数据持久化


## 关键要点回顾

| 概念 | 核心作用 | 关键 API |
|------|---------|---------|
| 依赖注入 | 代码复用、解耦、可测试 | `Depends()`, `yield`, `dependency_overrides` |
| 中间件 | 全局请求/响应处理 | `@app.middleware("http")`, `call_next` |
| 安全认证 | 身份验证与权限控制 | `OAuth2PasswordBearer`, JWT, `Security()` |
| 数据库集成 | 数据持久化 | `AsyncSession`, `get_db`, ORM 模型 |

## 下一步

恭喜你走完了 FastAPI 进阶之路。你已经掌握了构建生产级 API 的四大核心能力。接下来可以探索的方向：

- **后台任务**：用 `BackgroundTasks` 处理发邮件、生成报表等异步操作
- **WebSocket**：实现实时通信（聊天、推送通知）
- **缓存策略**：用 Redis 缓存高频查询结果
- **Docker 部署**：容器化你的 FastAPI 应用
- **CI/CD**：自动化测试和部署流水线