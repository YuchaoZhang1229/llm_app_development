## FastAPI 常用依赖注入速查表
| 依赖模式 | 典型写法 | 适用场景 |
|---|---|---|
| 函数依赖 | `def common_params(...): return {...}` | 抽取分页、查询参数、公共校验 |
| 数据库会话 | `def get_db(): ... yield db ...` | 每个请求获取并释放 DB 会话 |
| 用户认证 | `def get_current_user(token=Header(...))` | 解析 Token、获取当前用户 |
| 权限校验 | `def require_admin(user=Depends(get_current_user))` | 角色/权限检查，失败直接拦截 |
| 子依赖/依赖链 | 依赖函数里继续用 `Depends()` | 先取会话，再取用户，再校验权限 |
| 类依赖 | `class ItemService: ...` | 封装服务层、Repository、业务逻辑 |
| 参数化依赖 | `__call__` 实例或闭包工厂 | 传入固定配置、阈值、资源名等 |
| 全局/路由组依赖 | `FastAPI(dependencies=[...])` | 全局鉴权、日志、限流等副作用 |
| 测试覆盖依赖 | `app.dependency_overrides[...]` | 用假 DB、假用户替换真实依赖 |

