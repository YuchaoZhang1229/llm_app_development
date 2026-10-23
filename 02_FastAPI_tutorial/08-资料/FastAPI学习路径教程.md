# FastAPI 知识点学习路径教程（在职人员版）

## 前言：为什么在职开发者应该学 FastAPI

FastAPI 是目前 Python 生态中发展最快、社区最活跃的新一代 Web 框架。截至 2025 年，其 GitHub Star 数已超过 80k，微软、Netflix、滴滴等企业均已在生产环境中使用。它基于 Starlette（异步 Web 框架）和 Pydantic（数据校验库）构建，以**类型提示驱动、自动生成文档、原生异步高性能**为核心特性，迅速成为构建 REST API 和微服务的首选框架。

对于在职开发者来说，FastAPI 有几个特别值得投入时间的理由：

- **学习曲线平缓**：如果你已有 Python 基础，FastAPI 的上手速度远快于 Django，1-2 周即可写出可用接口。
- **即学即用**：自动生成交互式 API 文档（Swagger UI），写完代码就能在浏览器里测试，省去了手写文档的麻烦。
- **生产就绪**：原生异步支持 + 强类型校验，从开发小工具到承接高并发业务都能胜任。
- **职业竞争力**：越来越多的团队在技术选型中倾向 FastAPI，掌握它能为你的技术栈增加有分量的筹码。

本教程专为在职人员设计，假设你具备基本的 Python 编程能力（了解函数、类、列表/字典等数据结构），按照 10 周的学习路径，从零基础一路走到生产部署。每周只需投入 5-8 小时，利用工作日晚间和周末的碎片时间即可完成。

---

## 第一章：FastAPI 概览与环境搭建（第 1 周）

> **知识总览**
>
> | 知识点 | 功能说明 |
> |--------|----------|
> | FastAPI 框架定位 | 了解 FastAPI 在 Python Web 生态中的位置，与 Flask、Django 的区别和适用场景 |
> | 核心特性 | 高性能（ASGI）、自动文档（Swagger/ReDoc）、类型校验（Pydantic）、原生异步、依赖注入 |
> | ASGI vs WSGI | 理解异步服务器网关接口与传统同步标准的本质差异，掌握异步并发的基本原理 |
> | 环境搭建 | Python 3.10+ 虚拟环境创建、FastAPI 与 Uvicorn 安装、项目初始化 |
> | Uvicorn 服务器 | 了解 ASGI 服务器的角色，掌握开发模式启动命令和参数含义 |
> | 自动文档体验 | 访问 `/docs`（Swagger UI）和 `/redoc`（ReDoc），在浏览器中交互式测试接口 |
> | 第一个 API | 编写最小可运行的 GET 接口，理解装饰器路由定义和 JSON 响应 |

### 1.1 FastAPI 的核心特性

| 特性 | 说明 |
|------|------|
| 高性能 | 基于 ASGI，性能接近 Node.js 和 Go，是 Python Web 框架的性能天花板 |
| 自动文档 | 基于 OpenAPI 标准，自动生成 Swagger UI（`/docs`）和 ReDoc（`/redoc`） |
| 类型校验 | 利用 Python 类型提示 + Pydantic，请求参数自动校验、自动补全 |
| 原生异步 | 完全支持 `async/await`，适合高并发 I/O 密集型场景 |
| 依赖注入 | 灵活直观的依赖注入系统，轻松实现鉴权、分页、资源管理等横切逻辑 |
| 标准兼容 | 完全兼容 OpenAPI 和 JSON Schema 标准 |

### 1.2 与 Flask、Django 的横向对比

| 维度 | FastAPI | Flask | Django |
|------|---------|-------|--------|
| 性能 | 高（ASGI 异步） | 中（WSGI 同步） | 中（WSGI 同步） |
| 学习曲线 | 低-中 | 低 | 高 |
| 自动文档 | 内置 Swagger + ReDoc | 需第三方库 | 需第三方库 |
| 数据校验 | Pydantic（内置） | 手动或第三方 | Django Forms |
| 异步支持 | 原生 | 有限 | 有限 |
| 生态成熟度 | 快速增长 | 成熟 | 最成熟 |
| 适用场景 | API / 微服务 / AI 服务 | 小型 Web 应用 | 全栈 Web 应用 |

### 1.3 环境搭建

**Python 版本要求**：Python 3.10+（推荐 3.11 或更高，兼容性和性能更优）。

**第一步：创建项目目录和虚拟环境**

```bash
mkdir fastapi-learning && cd fastapi-learning
python -m venv venv

# 激活虚拟环境
# Linux / macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate
```

**第二步：安装核心依赖**

```bash
pip install fastapi uvicorn[standard]
```

- `fastapi`：框架本身
- `uvicorn[standard]`：ASGI 服务器，`[standard]` 包含所有可选的高性能依赖

**第三步：编写第一个接口**

创建 `main.py`：

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
```

**第四步：启动服务**

```bash
uvicorn main:app --reload --port 8000
```

- `main:app`：`main` 是文件名，`app` 是 FastAPI 实例
- `--reload`：开发模式，代码修改后自动重启（生产环境不要用）

启动后访问：

- `http://127.0.0.1:8000` — 你的接口
- `http://127.0.0.1:8000/docs` — Swagger UI 交互式文档
- `http://127.0.0.1:8000/redoc` — ReDoc 文档

打开 `/docs` 页面，你会看到自动生成的交互式 API 文档，可以直接在浏览器中发送请求测试接口——这就是 FastAPI 最让人省心的地方。

### 1.4 理解 ASGI 与 WSGI 的区别

作为在职开发者，理解框架底层的工作模型很重要：

- **WSGI**（Web Server Gateway Interface）：传统 Python Web 标准，同步处理，每个请求占用一个线程。Flask、Django 默认基于此。
- **ASGI**（Asynchronous Server Gateway Interface）：异步标准，支持 `async/await`、WebSocket、长连接。FastAPI 基于此。

简单理解：WSGI 像一条车道一次过一辆车，ASGI 像多车道并行，同一时间可以处理更多请求。在 I/O 密集型场景（数据库查询、调用外部 API）中，ASGI 的并发优势尤其明显。

### 1.5 本周实战建议

搭建一个个人信息接口服务：实现 `/me`（返回个人简介）、`/skills`（返回技能列表）、`/contact`（返回联系方式）三个 GET 接口，熟悉路由定义和 JSON 返回格式。

---

## 第二章：路由与请求处理（第 2 周）

> **知识总览**
>
> | 知识点 | 功能说明 |
> |--------|----------|
> | 路由定义 | 使用 `@app.get/post/put/patch/delete` 装饰器定义 RESTful 接口 |
> | async def vs def | 理解异步路由与同步路由的区别及适用场景 |
> | 路径参数 | 通过 `{参数名}` 捕获 URL 路径中的变量，支持类型转换和约束（Path） |
> | 查询参数 | 通过 URL 查询字符串传递参数，支持默认值、必填、范围约束（Query） |
> | 请求体（Body） | 用 Pydantic 模型定义 JSON 请求体，自动解析和校验 |
> | Form 表单 | 接收 `application/x-www-form-urlencoded` 格式的表单数据 |
> | 文件上传 | 使用 `UploadFile` 处理文件上传，支持读取内容和获取元信息 |
> | 响应模型 | 通过 `response_model` 精确控制返回数据结构，过滤敏感字段 |
> | 状态码控制 | 自定义 HTTP 状态码，使用 `JSONResponse` 返回不同响应 |

### 2.1 路由定义基础

FastAPI 使用装饰器定义路由，支持所有标准 HTTP 方法：

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/items")          # 查询
async def list_items():
    return [{"id": 1, "name": "item1"}]

@app.post("/items")         # 创建
async def create_item():
    return {"id": 2, "name": "new item"}

@app.put("/items/{item_id}")    # 更新（全量）
async def update_item(item_id: int):
    return {"item_id": item_id, "updated": True}

@app.patch("/items/{item_id}")  # 更新（部分）
async def patch_item(item_id: int):
    return {"item_id": item_id, "patched": True}

@app.delete("/items/{item_id}") # 删除
async def delete_item(item_id: int):
    return {"item_id": item_id, "deleted": True}
```

**`async def` vs `def`**：

- 如果你的函数不涉及 I/O 等待（数据库查询、网络请求），用 `def` 即可
- 如果涉及异步操作，用 `async def`
- FastAPI 会自动处理两者，不会搞混

### 2.2 路径参数

路径参数是 URL 路径中的一部分，用 `{参数名}` 标记：

```python
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    return {"user_id": user_id}
```

访问 `/users/42`，`user_id` 自动解析为整数 `42`。如果传入 `/users/abc`，FastAPI 会自动返回 422 错误，提示类型不匹配。

**支持的路径参数类型**：`int`、`float`、`str`、`bool`、`uuid.UUID`、`datetime` 等。

**添加参数约束**（通过 `Path`）：

```python
from fastapi import Path

@app.get("/users/{user_id}")
async def get_user(
    user_id: int = Path(ge=1, le=10000, description="用户ID，范围1-10000")
):
    return {"user_id": user_id}
```

### 2.3 查询参数

不在路径中、通过 URL 查询字符串传递的参数（`?key=value`）：

```python
from fastapi import Query

@app.get("/items")
async def list_items(
    page: int = Query(default=1, ge=1, description="页码"),
    size: int = Query(default=10, ge=1, le=100, description="每页数量"),
    q: str | None = Query(default=None, description="搜索关键词")
):
    return {"page": page, "size": size, "query": q}
```

访问 `/items?page=2&size=20&q=fastapi`，参数自动解析、自动校验。

**关键区分**：FastAPI 会根据参数是否在路径中定义来自动判断它是路径参数还是查询参数。没出现在路径 `{}` 中的参数就是查询参数。

### 2.4 请求体（Body）

用 Pydantic 模型定义请求体，这是 FastAPI 最强大的特性之一：

```python
from pydantic import BaseModel

class ItemCreate(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.post("/items")
async def create_item(item: ItemCreate):
    total = item.price + (item.tax or 0)
    return {"item": item.model_dump(), "total_price": total}
```

客户端发送 JSON 请求体，FastAPI 会自动：

1. 解析 JSON
2. 校验数据类型和约束
3. 将结果转为 Pydantic 模型实例

如果数据不合法（如缺少 `name` 字段、`price` 为字符串），自动返回 422 错误和详细的校验信息。

### 2.5 表单数据与文件上传

**表单数据**：

```python
from fastapi import Form

@app.post("/login")
async def login(
    username: str = Form(...),
    password: str = Form(...)
):
    return {"username": username}
```

**文件上传**：

```python
from fastapi import File, UploadFile

@app.post("/upload")
async def upload_file(file: UploadFile):
    contents = await file.read()
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(contents)
    }
```

### 2.6 响应模型与状态码

用 `response_model` 精确控制返回数据的结构，避免敏感信息泄露：

```python
from pydantic import BaseModel, EmailStr

class UserIn(BaseModel):
    username: str
    email: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: str

@app.post("/users", response_model=UserOut, status_code=201)
async def create_user(user: UserIn):
    # 模拟保存到数据库
    saved_user = {"id": 1, **user.model_dump()}
    return saved_user  # password 字段会被 response_model 自动过滤
```

**自定义不同状态的响应**：

```python
from fastapi.responses import JSONResponse

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    if item_id > 100:
        return JSONResponse(status_code=404, content={"detail": "Item not found"})
    return {"item_id": item_id}
```

### 2.7 本周实战建议

开发一个**待办事项管理 API**，包含：

- `POST /todos` — 创建待办（标题、描述、优先级）
- `GET /todos` — 列出所有待办（支持分页和按优先级筛选）
- `GET /todos/{todo_id}` — 获取单个待办
- `PUT /todos/{todo_id}` — 更新待办
- `DELETE /todos/{todo_id}` — 删除待办

先用内存列表模拟数据库，重点关注路由定义、参数校验和响应模型。

---

## 第三章：Pydantic 数据校验深入（第 3 周）

> **知识总览**
>
> | 知识点 | 功能说明 |
> |--------|----------|
> | Pydantic v2 核心变化 | v1 → v2 的 API 迁移（model_dump、field_validator 等），Rust 引擎带来的性能提升 |
> | BaseModel | Pydantic 模型基类，定义数据结构和字段类型 |
> | Field 约束 | 字段级校验（min_length、ge/le、pattern、default_factory）和文档描述 |
> | field_validator | 字段级自定义校验器，校验单个字段的业务规则 |
> | model_validator | 模型级校验器，实现跨字段校验（如确认密码一致性） |
> | 嵌套模型 | 定义包含子模型的复杂数据结构，递归校验 |
> | pydantic-settings | 通过 `BaseSettings` 管理环境变量和配置文件，自动类型转换 |

### 3.1 Pydantic v2 核心变化

FastAPI 从 0.100.0 版本开始正式支持 Pydantic v2。v2 的核心引擎用 Rust 重写（pydantic-core），性能提升显著——纯数据校验场景下可达 v1 的 20 倍以上。

**关键变化**：

- `dict()` → `model_dump()`
- `json()` → `model_dump_json()`
- `parse_obj()` → `model_validate()`
- `@validator` → `@field_validator`
- `@root_validator` → `@model_validator`

### 3.2 BaseModel 与 Field 详解

```python
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

class UserProfile(BaseModel):
    id: int
    username: str = Field(min_length=3, max_length=20, description="用户名")
    email: EmailStr = Field(description="邮箱地址")
    age: int = Field(ge=0, le=150, description="年龄")
    bio: str | None = Field(default=None, max_length=500, description="个人简介")
    created_at: datetime = Field(default_factory=datetime.now)
```

`Field` 支持的常用约束：

| 约束 | 适用类型 | 说明 |
|------|----------|------|
| `min_length` / `max_length` | str, list | 最小/最大长度 |
| `ge` / `gt` / `le` / `lt` | int, float | 大于等于/大于/小于等于/小于 |
| `pattern` | str | 正则表达式匹配 |
| `default` | 所有类型 | 默认值 |
| `default_factory` | 所有类型 | 默认值工厂函数 |
| `description` | 所有类型 | 字段描述（用于文档生成） |

### 3.3 自定义校验器

**字段级校验**（`@field_validator`）：

```python
from pydantic import BaseModel, field_validator

class UserRegister(BaseModel):
    username: str
    password: str
    confirm_password: str

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        if v.isdigit():
            raise ValueError("用户名不能全是数字")
        if len(v) < 3:
            raise ValueError("用户名至少3个字符")
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("密码至少8位")
        if not any(c.isupper() for c in v):
            raise ValueError("密码必须包含大写字母")
        return v
```

**模型级校验**（`@model_validator`）—— 用于跨字段校验：

```python
from pydantic import BaseModel, model_validator

class UserRegister(BaseModel):
    password: str
    confirm_password: str

    @model_validator(mode="after")
    def check_passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError("两次密码不一致")
        return self
```

### 3.4 嵌套模型与复杂结构

```python
from pydantic import BaseModel

class Address(BaseModel):
    city: str
    street: str
    zipcode: str

class Company(BaseModel):
    name: str
    address: Address

class Employee(BaseModel):
    name: str
    skills: list[str]
    company: Company
```

FastAPI 会自动递归校验嵌套结构，确保每一层数据都合法。

### 3.5 配置管理：pydantic-settings

项目中通常需要读取环境变量、配置文件。`pydantic-settings` 是最佳实践：

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "My FastAPI App"
    database_url: str
    secret_key: str
    debug: bool = False
    redis_url: str = "redis://localhost:6379"

    model_config = {"env_file": ".env"}

settings = Settings()
```

在项目根目录创建 `.env` 文件：

```
DATABASE_URL=postgresql://user:pass@localhost/mydb
SECRET_KEY=your-secret-key-here
DEBUG=true
```

这样配置和代码完全分离，环境变量自动加载、自动类型转换。

### 3.6 本周实战建议

为待办事项 API 加上完善的数据校验：

- 定义 `TodoCreate`、`TodoUpdate`、`TodoResponse` 三个模型
- 标题长度限制 1-100 字符
- 优先级只能是 1-5 的整数
- 截止日期不能早于今天
- 使用 `pydantic-settings` 管理项目配置

---

## 第四章：依赖注入系统（第 3-4 周）

> **知识总览**
>
> | 知识点 | 功能说明 |
> |--------|----------|
> | Depends 核心机制 | 依赖注入的入口，声明路由函数"需要什么"，框架自动准备并注入 |
> | 函数依赖 | 最常用写法，将通用逻辑（分页、校验）封装为独立函数 |
> | 类依赖 | 用类作为依赖项，适合有状态、多方法的复杂公共逻辑 |
> | 子依赖（依赖链） | 依赖本身也可以声明依赖，形成层次化的依赖树（如：获取用户→检查角色→检查权限） |
> | 全局依赖 | 通过 `dependencies` 参数对整个路由模块统一注入依赖 |
> | yield 依赖 | 使用 `yield` 管理资源生命周期（"进入时创建，退出时清理"），适合数据库会话、文件句柄等 |
> | 依赖覆盖 | 通过 `dependency_overrides` 在测试时替换依赖项，实现 Mock |
> | Token 鉴权依赖 | 使用 `OAuth2PasswordBearer` 和 JWT 实现可复用的认证依赖 |

依赖注入是 FastAPI 最核心的设计之一，也是写好工程化代码的关键。理解了它，你的代码会从"能用"跃升到"好维护"。

### 4.1 核心思想

在没有依赖注入的情况下，公共逻辑（鉴权、分页、日志）会在每个路由函数里重复出现。依赖注入的思路是：**把公共逻辑抽离为独立的函数/类，路由声明"我需要什么"，框架自动帮你准备好**。

```python
from fastapi import Depends

# 定义依赖
def common_params(
    page: int = 1,
    size: int = 10
) -> dict:
    return {"page": page, "size": min(size, 100)}

# 路由使用依赖
@app.get("/items")
def list_items(params: dict = Depends(common_params)):
    return {"params": params}
```

`Depends` 做了什么：当请求到达时，FastAPI 先调用 `common_params`，拿到返回值，然后把它注入到 `list_items` 的 `params` 参数中。

### 4.2 四种依赖写法

**函数依赖**（最常用）——适合简单的通用逻辑：

```python
def get_pagination(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100)
):
    return {"page": page, "size": size, "offset": (page - 1) * size}
```

**类依赖**——适合有状态、多方法的复杂逻辑：

```python
class Pagination:
    def __init__(self, page: int = 1, size: int = 10):
        self.page = page
        self.size = min(size, 100)

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.size

@app.get("/items")
def list_items(pager: Pagination = Depends()):
    return {"offset": pager.offset, "size": pager.size}
```

**子依赖（依赖链）**——依赖本身也可以有依赖：

```python
from fastapi import Header, HTTPException

def get_current_user(token: str = Header(...)):
    user = verify_token(token)  # 伪代码
    if not user:
        raise HTTPException(status_code=401, detail="无效Token")
    return user

def get_admin_user(user: dict = Depends(get_current_user)):
    if "admin" not in user.get("roles", []):
        raise HTTPException(status_code=403, detail="权限不足")
    return user

@app.delete("/users/{user_id}")
def delete_user(user_id: int, admin: dict = Depends(get_admin_user)):
    return {"deleted": user_id}
```

FastAPI 会自动解析整条依赖链：先获取 token → 验证用户 → 检查管理员权限 → 全部通过后才执行路由函数。

**全局依赖**——对整个路由模块生效：

```python
router = APIRouter(
    prefix="/admin",
    tags=["后台管理"],
    dependencies=[Depends(get_current_user)]  # 该模块所有接口都需要登录
)
```

### 4.3 yield 依赖与资源管理

`yield` 让依赖项可以管理资源的生命周期——"进入时创建，退出时清理"：

```python
from sqlalchemy.orm import Session

def get_db():
    db = SessionLocal()
    try:
        yield db           # 把 db 注入给路由
        db.commit()        # 请求成功则提交
    except Exception:
        db.rollback()      # 出错则回滚
        raise
    finally:
        db.close()         # 无论如何都关闭连接
```

这是管理数据库会话、文件句柄、网络连接等有状态资源的最佳模式。

### 4.4 依赖注入实战：Token 鉴权

```python
from fastapi import Header, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_jwt(token)  # 解析 JWT
    if payload is None:
        raise HTTPException(status_code=401, detail="无效Token")
    user = await get_user_by_id(payload["user_id"])
    if user is None:
        raise HTTPException(status_code=401, detail="用户不存在")
    return user

@app.get("/me")
async def read_me(current_user: dict = Depends(get_current_user)):
    return current_user
```

### 4.5 依赖覆盖（测试利器）

FastAPI 允许在测试时替换依赖项，这是写测试的关键：

```python
# 测试中替换数据库依赖
app.dependency_overrides[get_db] = lambda: Session(testing_engine)
# 测试中替换鉴权依赖
app.dependency_overrides[get_current_user] = lambda: {"id": 1, "username": "test"}
```

### 4.6 本周实战建议

为待办事项 API 添加：

- 统一的分页依赖
- 模拟用户登录依赖（返回固定用户信息）
- 需要登录才能创建/删除待办
- 不同用户只能操作自己的待办

---

## 第五章：数据库集成（第 4-5 周）

> **知识总览**
>
> | 知识点 | 功能说明 |
> |--------|----------|
> | 数据库技术选型 | 了解 PostgreSQL / MySQL / SQLite / MongoDB / Redis 各自适用场景和推荐驱动 |
> | SQLAlchemy 2.0 异步 | 使用 `create_async_engine` + `async_sessionmaker` 构建异步数据库连接 |
> | ORM 模型定义 | 用 SQLAlchemy 声明式语法定义数据表结构、字段类型和索引 |
> | 数据库会话管理 | 通过 `yield` 依赖实现会话的自动创建、提交/回滚和关闭 |
> | Alembic 迁移 | 使用 Alembic 生成和执行数据库迁移脚本，管理表结构变更 |
> | Repository 模式 | 将数据库 CRUD 操作封装为独立的仓库层，路由不直接操作数据库 |
> | SQLModel | FastAPI 作者开发的 ORM + Pydantic 合一库，减少样板代码 |

### 5.1 技术选型

FastAPI 不绑定任何特定数据库，但以下是主流选择：

| 数据库 | 推荐 ORM / 驱动 | 适用场景 |
|--------|----------------|----------|
| PostgreSQL | SQLAlchemy 2.0 + asyncpg | 生产环境首选 |
| MySQL | SQLAlchemy 2.0 + aiomysql | 已有 MySQL 基础设施 |
| SQLite | SQLAlchemy + aiosqlite | 开发/测试/小型项目 |
| MongoDB | motor（异步驱动） | 文档型数据 |
| Redis | redis-py（异步） | 缓存、会话管理 |

### 5.2 SQLAlchemy 2.0 异步集成

**安装**：

```bash
pip install sqlalchemy[asyncio] asyncpg
```

**数据库引擎与会话工厂**（`app/db/session.py`）：

```python
from sqlalchemy.ext.asyncio import (
    AsyncSession, async_sessionmaker, create_async_engine
)

DATABASE_URL = "postgresql+asyncpg://user:pass@localhost/mydb"

engine = create_async_engine(DATABASE_URL, pool_pre_ping=True)
AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
```

**定义 ORM 模型**（`app/models.py`）：

```python
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(String(500))
    completed = Column(Boolean, default=False)
    priority = Column(Integer, default=3)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
```

### 5.3 Alembic 数据库迁移

Alembic 是 SQLAlchemy 官方推荐的迁移工具：

```bash
pip install alembic
alembic init alembic
```

配置 `alembic.ini` 中的数据库连接，然后：

```bash
# 自动生成迁移脚本
alembic revision --autogenerate -m "create todos table"
# 执行迁移
alembic upgrade head
# 回滚
alembic downgrade -1
```

### 5.4 Repository 模式

将数据库操作封装为独立的仓库层，路由不直接操作数据库：

```python
# app/repositories/todo_repo.py
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

class TodoRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self, user_id: int, page: int, size: int):
        offset = (page - 1) * size
        stmt = (
            select(Todo)
            .where(Todo.user_id == user_id)
            .offset(offset)
            .limit(size)
            .order_by(Todo.created_at.desc())
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create(self, todo_data: dict, user_id: int) -> Todo:
        todo = Todo(**todo_data, user_id=user_id)
        self.session.add(todo)
        await self.session.flush()
        return todo
```

### 5.5 SQLModel 简介

SQLModel 由 FastAPI 的作者开发，将 SQLAlchemy 和 Pydantic 合二为一：

```python
from sqlmodel import SQLModel, Field

class Todo(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(max_length=100)
    description: str | None = Field(default=None, max_length=500)
    completed: bool = False
```

同一个模型既可以做数据库 ORM，又可以做 API 数据校验，减少了样板代码。适合中小型项目快速开发。

### 5.6 本周实战建议

将待办事项 API 从内存存储迁移到 PostgreSQL（本地可用 SQLite 替代），实现完整的数据持久化。练习 Alembic 迁移、Repository 模式封装、数据库会话依赖注入。

---

## 第六章：认证与安全（第 5-6 周）

> **知识总览**
>
> | 知识点 | 功能说明 |
> |--------|----------|
> | JWT 认证原理 | 理解 JSON Web Token 的签发、携带和验证流程 |
> | OAuth2 密码模式 | 使用 `OAuth2PasswordBearer` 和 `OAuth2PasswordRequestForm` 实现标准认证流 |
> | 密码哈希 | 使用 `passlib` + `bcrypt` 安全存储密码，禁止明文存储 |
> | Token 签发与验证 | 用 `PyJWT` 创建和解析 access_token，处理过期和无效 Token |
> | 角色与权限控制 | 实现基于角色的访问控制（RBAC），工厂函数动态生成权限依赖 |
> | CORS 跨域配置 | 使用 `CORSMiddleware` 控制前端域名访问权限 |
> | 速率限制 | 使用 `slowapi` 防止接口被恶意刷取 |
> | 安全最佳实践 | HTTPS、密钥管理、敏感数据脱敏、输入校验等生产安全清单 |

### 6.1 JWT 认证流程

JWT（JSON Web Token）是 API 认证的主流方案，流程如下：

```
客户端 → 发送用户名/密码 → POST /auth/login
服务端 → 验证凭据 → 签发 JWT（access_token）
客户端 → 携带 JWT 请求 → Authorization: Bearer <token>
服务端 → 验证 JWT → 提取用户信息 → 处理请求
```

### 6.2 完整实现

```python
import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# 密码哈希
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

# JWT 签发与验证
SECRET_KEY = "your-secret-key"  # 生产环境用环境变量
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=30))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None
```

### 6.3 登录接口与保护路由

```python
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@app.post("/auth/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    token = create_access_token(data={"sub": user["username"]})
    return {"access_token": token, "token_type": "bearer"}

async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="无效Token")
    username = payload.get("sub")
    if username is None:
        raise HTTPException(status_code=401, detail="Token格式错误")
    user = await get_user_by_username(username)
    if user is None:
        raise HTTPException(status_code=401, detail="用户不存在")
    return user

@app.get("/me")
async def read_me(user: dict = Depends(get_current_user)):
    return {"username": user["username"], "email": user["email"]}
```

### 6.4 角色与权限控制

```python
def require_role(*roles: str):
    """工厂函数：生成角色检查依赖"""
    async def role_checker(
        current_user: dict = Depends(get_current_user)
    ):
        if current_user.get("role") not in roles:
            raise HTTPException(status_code=403, detail="权限不足")
        return current_user
    return role_checker

@app.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    admin: dict = Depends(require_role("admin"))
):
    # 只有管理员能执行
    ...
```

### 6.5 安全最佳实践

- **CORS 配置**：明确指定允许的前端域名，不要用 `allow_origins=["*"]`
- **速率限制**：使用 `slowapi` 库防止接口被恶意刷取
- **HTTPS**：生产环境必须启用 HTTPS
- **密钥管理**：SECRET_KEY、数据库密码等通过环境变量注入，绝不硬编码
- **密码哈希**：始终使用 bcrypt 或 argon2，不要自己实现哈希逻辑

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 6.6 本周实战建议

为项目添加完整的认证系统：用户注册（密码哈希存储）、登录（JWT 签发）、获取当前用户、管理员权限控制。在 Swagger UI 中测试带认证的接口。

---

## 第七章：中间件与工程化（第 6-7 周）

> **知识总览**
>
> | 知识点 | 功能说明 |
> |--------|----------|
> | 中间件原理 | 理解"洋葱模型"——请求进入和响应返回时中间件的执行顺序 |
> | 内置中间件 | 使用 CORS、GZip、TrustedHost 中间件处理跨域、压缩和安全 |
> | 自定义中间件 | 通过 `BaseHTTPMiddleware` 实现请求日志、计时、异常捕获等横切逻辑 |
> | 分层项目结构 | Router → Service → Repository → Model 的职责分离和目录组织 |
> | API 版本控制 | 通过路由前缀（`/api/v1`、`/api/v2`）实现多版本 API 共存 |
> | 统一异常处理 | 自定义异常类 + `@app.exception_handler` 实现全局错误响应格式 |
> | 配置管理 | 使用 pydantic-settings + `.env` 文件实现环境隔离的配置注入 |

### 7.1 中间件原理

中间件是在每个请求到达路由处理函数之前和之后执行的函数。执行流程可以理解为"洋葱模型"：

```
请求进入 → 中间件A(前) → 中间件B(前) → 路由处理函数
响应返回 ← 中间件A(后) ← 中间件B(后) ←
```

### 7.2 内置中间件

```python
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

# CORS：跨域资源共享
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"])

# GZip：自动压缩响应（>1KB）
app.add_middleware(GZipMiddleware, minimum_size=1000)

# TrustedHost：限制请求的 Host 头
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["your-domain.com"])
```

### 7.3 自定义中间件

**请求日志中间件**：

```python
import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class RequestLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.time()
        response = await call_next(request)
        duration = time.time() - start
        print(
            f"{request.method} {request.url.path} "
            f"- {response.status_code} "
            f"- {duration:.4f}s"
        )
        return response

app.add_middleware(RequestLogMiddleware)
```

### 7.4 项目结构分层

随着项目规模增长，所有代码堆在一个文件里会难以维护。推荐按业务域分包的分层结构：

```
project_root/
├── app/
│   ├── main.py              # 应用入口，注册路由和中间件
│   ├── core/
│   │   ├── config.py        # 配置管理
│   │   ├── security.py      # 安全相关（JWT、密码）
│   │   └── deps.py          # 全局依赖项
│   ├── api/
│   │   └── v1/
│   │       ├── router.py    # v1 路由汇总
│   │       ├── auth.py      # 认证路由
│   │       └── todos.py     # 待办路由
│   ├── models/
│   │   └── todo.py          # ORM 模型
│   ├── schemas/
│   │   ├── todo.py          # Pydantic 模型
│   │   └── user.py
│   ├── services/
│   │   └── todo_service.py  # 业务逻辑层
│   ├── repositories/
│   │   └── todo_repo.py     # 数据访问层
│   └── db/
│       ├── session.py        # 数据库会话
│       └── base.py           # ORM 基类
├── alembic/                   # 数据库迁移
├── tests/                     # 测试
├── .env                       # 环境变量
└── requirements.txt           # 依赖列表
```

**分层职责**：

| 层级 | 职责 | 原则 |
|------|------|------|
| API 层（Router） | 处理 HTTP 请求、参数校验、响应序列化 | 不包含业务逻辑 |
| Service 层 | 核心业务逻辑 | 不关心 HTTP 细节 |
| Repository 层 | 数据库 CRUD 操作 | 不包含业务判断 |
| Model 层 | 数据结构定义 | ORM 模型和 Pydantic 模型分开 |

### 7.5 API 版本控制

```python
from fastapi import APIRouter

api_v1 = APIRouter(prefix="/api/v1")
api_v2 = APIRouter(prefix="/api/v2")

api_v1.include_router(auth_router)
api_v1.include_router(todo_router)

app.include_router(api_v1)
app.include_router(api_v2)
```

### 7.6 统一异常处理

```python
from fastapi import Request
from fastapi.responses import JSONResponse

class AppException(Exception):
    def __init__(self, code: str, message: str, status_code: int = 400):
        self.code = code
        self.message = message
        self.status_code = status_code

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.code,
            "message": exc.message,
            "path": str(request.url.path)
        }
    )
```

### 7.7 本周实战建议

重构待办事项 API：

- 采用分层项目结构
- 添加请求日志中间件
- 实现统一异常处理
- 配置 API 版本控制（`/api/v1/todos`）

---

## 第八章：高级特性（第 7-8 周）

> **知识总览**
>
> | 知识点 | 功能说明 |
> |--------|----------|
> | WebSocket | 实现客户端与服务端的双向长连接，支持实时通信（聊天、通知、协作） |
> | ConnectionManager | 管理 WebSocket 连接的建立、断开和消息广播 |
> | BackgroundTasks | 内置后台任务，请求返回后异步执行耗时操作（发邮件、生成报告） |
> | Celery 任务队列 | 分布式异步任务处理，适合重量级后台作业（视频处理、批量导出） |
> | StreamingResponse | 流式响应，支持大文件下载、视频流、AI 模型的逐字输出 |
> | Server-Sent Events | 服务端单向推送事件流，适合实时数据更新通知 |
> | pytest + httpx 测试 | 使用异步测试客户端编写 API 测试，配合依赖覆盖实现 Mock |
> | 测试最佳实践 | fixture、标记（`@pytest.mark.asyncio`）、依赖覆盖、测试数据库隔离 |

### 8.1 WebSocket 实时通信

WebSocket 允许客户端和服务端保持双向长连接，适合聊天、实时通知、在线协作等场景：

```python
from fastapi import WebSocket, WebSocketDisconnect

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket)
    await manager.broadcast(f"{client_id} 加入了聊天室")
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"{client_id}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"{client_id} 离开了聊天室")
```

### 8.2 后台任务

FastAPI 内置 `BackgroundTasks`，适合发送通知邮件、生成报告等不需要等待完成的耗时操作：

```python
from fastapi import BackgroundTasks

def send_email(to: str, subject: str, body: str):
    # 模拟发送邮件（耗时操作）
    import time
    time.sleep(3)
    print(f"邮件已发送到 {to}")

@app.post("/register")
async def register(
    email: str,
    background_tasks: BackgroundTasks
):
    # 先返回响应，后台发邮件
    background_tasks.add_task(send_email, email, "欢迎", "感谢注册！")
    return {"message": "注册成功，确认邮件正在发送"}
```

**注意**：`BackgroundTasks` 适合轻量任务。对于重量级的异步任务（视频处理、批量导出等），应使用 Celery 或 ARQ 等专业任务队列。

### 8.3 异步任务队列（Celery）

```python
# celery_worker.py
from celery import Celery

celery_app = Celery("worker", broker="redis://localhost:6379/0")

@celery_app.task
def generate_report(user_id: int):
    # 耗时的报告生成逻辑
    ...
    return f"报告已生成: user_{user_id}"
```

```python
# 在路由中触发
@app.post("/reports")
async def create_report(user_id: int):
    task = generate_report.delay(user_id)  # 异步执行
    return {"task_id": task.id, "status": "processing"}
```

### 8.4 StreamingResponse 流式响应

适合大文件下载、视频流、AI 模型的流式输出等场景：

```python
from fastapi.responses import StreamingResponse
import asyncio

async def generate_data():
    for i in range(10):
        yield f"数据块 {i}\n"
        await asyncio.sleep(0.5)

@app.get("/stream")
async def stream_data():
    return StreamingResponse(
        generate_data(),
        media_type="text/plain"
    )
```

**AI 流式输出示例**（类似 ChatGPT 的逐字输出效果）：

```python
from fastapi.responses import StreamingResponse

async def generate_ai_response(prompt: str):
    # 模拟流式调用大模型 API
    words = ["这是", "一个", "流式", "输出", "的", "示例"]
    for word in words:
        yield word
        await asyncio.sleep(0.1)

@app.post("/chat/stream")
async def chat_stream(prompt: str):
    return StreamingResponse(
        generate_ai_response(prompt),
        media_type="text/event-stream"
    )
```

### 8.5 测试

FastAPI 推荐使用 `pytest` + `httpx`（异步测试客户端）进行测试：

```python
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

@pytest.mark.asyncio
async def test_create_todo(client: AsyncClient):
    response = await client.post(
        "/api/v1/todos",
        json={"title": "学习FastAPI", "priority": 5}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "学习FastAPI"

@pytest.mark.asyncio
async def test_list_todos(client: AsyncClient):
    response = await client.get("/api/v1/todos?page=1&size=10")
    assert response.status_code == 200
```

**测试中替换依赖**（Mock 数据库、Mock 用户）：

```python
from app.core.deps import get_db, get_current_user

@pytest.fixture(autouse=True)
def override_deps():
    app.dependency_overrides[get_current_user] = lambda: {
        "id": 1, "username": "test_user", "role": "admin"
    }
    yield
    app.dependency_overrides.clear()
```

### 8.6 本周实战建议

- 为项目添加 WebSocket 实时通知功能（待办状态变更时推送通知）
- 实现一个后台任务：创建待办后发送提醒邮件
- 编写完整的单元测试，覆盖 CRUD 接口和鉴权逻辑

---

## 第九章：部署与运维（第 9-10 周）

> **知识总览**
>
> | 知识点 | 功能说明 |
> |--------|----------|
> | Docker 容器化 | 编写 Dockerfile 将 FastAPI 应用打包为可移植的容器镜像 |
> | Gunicorn + UvicornWorker | 生产环境部署方案：Gunicorn 管理进程、UvicornWorker 运行异步应用 |
> | Worker 配置策略 | 根据 CPU 核心数和业务类型（I/O 密集/CPU 密集）确定 Worker 数量 |
> | Docker Compose | 编排 FastAPI + PostgreSQL + Redis 等多服务应用 |
> | Nginx 反向代理 | 配置请求转发、超时参数、WebSocket 代理支持 |
> | 异步最佳实践 | 避免在 async 路由中使用阻塞调用，正确使用 `run_in_executor` |
> | 性能优化 | 数据库连接池、Redis 缓存、GZip 压缩、预加载（`--preload`） |
> | 结构化日志 | 使用 `structlog` 记录请求方法、路径、状态码和耗时 |
> | Prometheus 监控 | 通过 `prometheus_fastapi_instrumentator` 暴露 `/metrics` 端点 |
> | CI/CD | GitHub Actions 自动化测试和部署流水线 |

### 9.1 Docker 容器化

创建 `Dockerfile`：

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential && \
    rm -rf /var/lib/apt/lists/*

# 安装 Python 依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目代码
COPY .. .

# 启动命令：Gunicorn + UvicornWorker
CMD ["gunicorn", "app.main:app", \
     "-w", "4", \
     "-k", "uvicorn.workers.UvicornWorker", \
     "-b", "0.0.0.0:8000", \
     "--timeout", "120", \
     "--max-requests", "1000", \
     "--max-requests-jitter", "50"]
```

**关键参数说明**：

| 参数 | 说明 | 推荐值 |
|------|------|--------|
| `-w` | Worker 进程数 | CPU 核心数 × 2（I/O 密集型） |
| `-k` | Worker 类型 | `uvicorn.workers.UvicornWorker` |
| `--timeout` | 请求超时（秒） | 120 |
| `--max-requests` | 单个 Worker 处理请求数后重启 | 1000（防内存泄漏） |

### 9.2 Docker Compose 编排

```yaml
version: "3.8"

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql+asyncpg://user:pass@db:5432/mydb
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis

  db:
    image: postgres:15
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: mydb
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine

volumes:
  postgres_data:
```

### 9.3 Nginx 反向代理

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # 超时设置
        proxy_read_timeout 300s;
        proxy_send_timeout 300s;
    }

    # WebSocket 支持
    location /ws {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

### 9.4 性能优化要点

**异步最佳实践**：

- `async def` 路由中**绝不使用**阻塞调用（`time.sleep()`、`requests.get()` 等）
- 需要调用同步库时，使用 `run_in_executor` 放到线程池
- 数据库操作一律使用异步驱动（asyncpg、aiosqlite、aiomysql）

```python
import asyncio

# 错误：阻塞整个事件循环
@app.get("/bad")
async def bad_endpoint():
    import time
    time.sleep(5)  # 千万不要这样做！
    return {"message": "done"}

# 正确：使用线程池执行阻塞操作
@app.get("/good")
async def good_endpoint():
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, blocking_function)
    return {"result": result}
```

**其他优化建议**：

- **连接池**：数据库连接使用连接池复用，避免每次请求都新建连接
- **Redis 缓存**：高频查询结果缓存到 Redis，减少数据库压力
- **GZip 压缩**：对大于 1KB 的响应启用 GZip
- **预加载**：Gunicorn 使用 `--preload` 参数，Worker 启动时预加载应用代码

### 9.5 日志与监控

**结构化日志**（使用 `structlog`）：

```python
import structlog

logger = structlog.get_logger()

@app.middleware("http")
async def log_requests(request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    logger.info(
        "request_completed",
        method=request.method,
        path=request.url.path,
        status=response.status_code,
        duration_ms=round(duration * 1000, 2)
    )
    return response
```

**Prometheus 监控**：

```python
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()
# ... 注册路由和中间件 ...
Instrumentator().instrument(app).expose(app, endpoint="/metrics")
```

这会暴露 `/metrics` 端点，Prometheus 可以抓取请求数、延迟、状态码分布等指标。

### 9.6 CI/CD 建议

推荐 GitHub Actions 或 GitLab CI，基本流水线：

```yaml
# .github/workflows/deploy.yml
name: Deploy
on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install -r requirements.txt
      - run: pytest tests/ -v

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build and push Docker image
        run: |
          docker build -t my-fastapi-app .
          docker push my-registry/my-fastapi-app
      - name: Deploy to server
        run: |
          ssh user@server "docker pull my-registry/my-fastapi-app && docker-compose up -d"
```

### 9.7 本周实战建议

- 编写 Dockerfile 和 docker-compose.yml
- 在本地用 Docker 跑起完整项目（FastAPI + PostgreSQL + Redis）
- 配置 Nginx 反向代理
- 添加 Prometheus 监控，用 Grafana 可视化

---

## 第十章：学习资源与进阶方向

> **知识总览**
>
> | 知识点 | 功能说明 |
> |--------|----------|
> | 官方文档体系 | 掌握 FastAPI 官方教程、用户指南和 API 参考的查阅方法 |
> | 社区资源 | 了解 GitHub 高星项目、推荐开源库（FastAPI Users、Cache、Pagination 等） |
> | 微服务架构 | FastAPI + gRPC + 消息队列的分布式系统设计方向 |
> | GraphQL 集成 | 使用 Strawberry 库在 FastAPI 中提供 GraphQL 接口 |
> | AI 模型服务 | 用 FastAPI 部署 TensorFlow / PyTorch 机器学习模型的推理接口 |
> | 全栈开发 | FastAPI + React/Vue 的前后端分离项目搭建 |
> | 学习路径回顾 | 10 周各阶段知识点串联和在职学习的时间管理建议 |

### 10.1 推荐学习资源

| 资源 | 说明 | 链接 |
|------|------|------|
| FastAPI 官方文档 | 最权威、最全面的学习资料 | https://fastapi.tiangolo.com |
| FastAPI 中文文档 | 官方文档的中文翻译 | https://fastapi.tiangolo.com/zh |
| FastAPI 官方教程 | 循序渐进的用户指南 | https://fastapi.tiangolo.com/tutorial |
| fastapi-best-practices | GitHub 高星项目，生产环境最佳实践 | https://github.com/zhanymkanov/fastapi-best-practices |
| Full Stack FastAPI Template | 官方全栈模板项目 | https://github.com/fastapi/full-stack-fastapi-template |

### 10.2 推荐开源项目参考

- **FastAPI Users**：开箱即用的用户认证系统
- **FastAPI Cache**：接口缓存方案
- **FastAPI Pagination**：自动分页处理
- **SQLModel**：SQLAlchemy + Pydantic 合一
- **Tortoise ORM**：纯异步 ORM，Django 风格

### 10.3 进阶方向

当掌握了本教程的内容后，可以根据工作需要选择深入的方向：

| 方向 | 技术栈 | 适用场景 |
|------|--------|----------|
| 微服务架构 | FastAPI + gRPC + RabbitMQ | 大规模分布式系统 |
| GraphQL API | FastAPI + Strawberry | 前端需要灵活查询 |
| AI 模型服务 | FastAPI + TensorFlow/PyTorch | 部署机器学习模型 |
| 实时应用 | FastAPI + WebSocket + Redis Pub/Sub | 聊天、协作、通知 |
| 全栈开发 | FastAPI + React/Vue + Docker | 独立开发者全栈项目 |

### 10.4 学习路径总结

```
第 1 周     环境搭建 + 基础路由 + 自动文档
第 2 周     路由深入 + 请求参数 + 响应模型
第 3 周     Pydantic 数据校验 + 配置管理
第 3-4 周   依赖注入系统（核心中的核心）
第 4-5 周   数据库集成 + 迁移 + Repository 模式
第 5-6 周   JWT 认证 + 权限控制 + 安全实践
第 6-7 周   中间件 + 工程化 + 项目结构
第 7-8 周   WebSocket + 后台任务 + 测试
第 9-10 周  Docker 部署 + Nginx + 监控
```

### 10.5 给在职学习者的建议

1. **不要试图一次学完**：按周推进，每周掌握一个阶段就足够。工作中用到的时候再回来深入对应章节。
2. **实战优先**：每章的实战建议一定要做，写代码比看教程有效 10 倍。
3. **从小工具开始**：先给自己的工作写个小 API（比如内部数据查询接口），比做大项目更容易坚持。
4. **善用官方文档**：FastAPI 的官方文档质量极高，遇到不确定的点优先查文档。
5. **加入社区**：GitHub Discussions、Reddit 的 r/FastAPI、知乎和掘金上都有活跃的 FastAPI 社区，遇到问题可以快速得到帮助。

---

## 参考文献

1. FastAPI 官方文档 — https://fastapi.tiangolo.com
2. FastAPI Tutorial User Guide — https://fastapi.tiangolo.com/tutorial/
3. FastAPI Best Practices (GitHub) — https://github.com/zhanymkanov/fastapi-best-practices
4. Mastering FastAPI: A Complete Learning Roadmap — https://dev.to/prasanna_kumar/mastering-fastapi-a-complete-learning-roadmap-477o
5. Pydantic V2 Documentation — https://docs.pydantic.dev/latest/
6. FastAPI 从入门到生产（腾讯云开发者社区） — https://cloud.tencent.com/developer/article/2613804

---

内容由 AI 生成
