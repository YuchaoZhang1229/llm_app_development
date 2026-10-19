# Python 学习路径 · 每个模块的知识点与学习重点（AI 应用 / Agent 开发方向）

> 适用对象：零基础起步、目标 AI 应用 / Agent 开发（LangChain · LangGraph）
> 使用方法：每个模块先过一遍「知识点清单」，再重点攻克 ⭐ 标注的「学习重点」，最后对照「常见坑」自查。

---

## 第 1 层 · 语言基础（01-04）

### 01 基础语法

| 类别 | 知识点 |
|------|--------|
| 变量与类型 | int / float / str / bool、动态类型、type() |
| 运算符 | 算术、比较、逻辑（and/or/not）、in / is |
| 控制流 | if / elif / else、for、while、break / continue |
| 字符串 | f-string 格式化、常用方法（split / strip / replace / join） |
| 输入输出 | print / input、基本调试 print 大法 |

⭐ **学习重点**
- **f-string 格式化**：Agent 日志、Prompt 拼接天天用，练到熟练。
- **字符串方法**（split / join / strip）：文本处理的地基，RAG 数据清洗的前置。
- 列表/字符串**切片**语法 `s[a:b:step]`：读框架源码常见。

⚠️ 常见坑：可变默认参数、`=` 与 `is` 混用、整数除法 `/` 与 `//` 区别。

---

### 02 数据结构

| 类别 | 知识点 |
|------|--------|
| 序列 | list（增删改查、append / extend / pop）、tuple（不可变、解包） |
| 映射 | dict（get / items / keys / values、setdefault） |
| 集合 | set（去重、交并差集） |
| 推导式 | 列表推导式、字典推导式、条件过滤 |
| 排序 | sorted / sort、key 参数、lambda |

⭐ **学习重点**
- **dict 操作**：LangChain 的消息历史、Tool 的参数、LangGraph 的 State 全是 dict，`get` / `items` / 解包必须滚瓜烂熟。
- **推导式**：把"循环 + append"一行化，框架源码里到处都是。
- **sorted 的 key 参数**：对消息列表、检索结果排序时高频使用。

⚠️ 常见坑：dict 遍历时增删键报错、浅拷贝 `copy()` 与深拷贝 `deepcopy` 的区别。

---

### 03 函数与作用域

| 类别 | 知识点 |
|------|--------|
| 定义与调用 | def、返回值、多返回值（元组解包） |
| 参数 | 位置参数、关键字参数、默认参数、`*args` / `**kwargs` |
| 作用域 | LEGB 规则、global / nonlocal |
| 函数是一等公民 | 函数作参数 / 返回值、lambda、闭包 |
| 文档 | docstring、类型注解初识 |

⭐ **学习重点**
- **`*args` / `**kwargs`**：框架封装、Tool 转发参数全靠它，必须彻底理解。
- **闭包**：装饰器的原理基础，学不透装饰器就卡壳。
- **函数作为参数**：LangChain 的 `Runnable`、回调机制都建立在"函数可传递"上。

⚠️ 常见坑：默认参数用可变对象（`def f(x=[])`）、闭包晚绑定问题。

---

### 04 面向对象

| 类别 | 知识点 |
|------|--------|
| 类基础 | class、`__init__`、self、实例属性 / 类属性 |
| 方法 | 实例方法、`@classmethod`、`@staticmethod` |
| 继承 | 单继承、多继承、`super()`、方法重写 |
| 魔法方法 | `__str__` / `__repr__`、`__len__`、`__call__`、`__eq__` |
| 进阶（补） | `@property`、抽象基类 ABC、`isinstance` 判断 |

⭐ **学习重点**
- **继承 + 方法重写**：LangChain 的用法本质是"继承 BaseTool / BaseModel 再重写方法"，这是 Agent 开发的核心套路。
- **`__call__`**：LangChain 的 `Runnable` 全靠它，让对象可以像函数一样被调用——`llm.invoke(x)` 背后就是 `__call__`。
- **ABC 抽象基类**：理解框架"为什么必须重写这个方法才能用"。
- **`@property`**：读框架源码常见，把方法伪装成属性。

⚠️ 常见坑：多继承的 MRO 顺序、类属性与实例属性混淆。

---

## 第 2 层 · 语言进阶（05-08）

### 05 高级特性（⭐ 全路线最重要的模块之一）

| 类别 | 知识点 |
|------|--------|
| 迭代器 | 可迭代对象 vs 迭代器、`__iter__` / `__next__`、iter() / next() |
| 生成器 | yield、生成器表达式、yield from、惰性求值 |
| 装饰器 | 闭包回顾、`@` 语法、带参数的装饰器、`functools.wraps` |
| 上下文管理器 | with 语句、`__enter__` / `__exit__`、contextlib |
| 函数式工具 | functools.partial、lru_cache |

⭐ **学习重点**
- **生成器 = Streaming 的底层**：LLM 逐 token 输出（`stream()` / `astream()`）就是生成器在驱动，必须亲手写几个 yield 例子。
- **装饰器**：`@tool`、`@retry`、`@cache` 等框架语法全是装饰器，要能自己写一个带参数的装饰器。
- **上下文管理器**：管理模型客户端、数据库连接、文件句柄的标准姿势。
- **迭代器协议**：看懂"为什么 for 能遍历一切"。

⚠️ 常见坑：生成器只能遍历一次、装饰器忘加 `functools.wraps` 丢失函数名。

---

### 06 异常处理

| 类别 | 知识点 |
|------|--------|
| 基础 | try / except / else / finally、常见异常类型 |
| 抛出 | raise、异常链（from e） |
| 自定义 | 自定义异常类（继承 Exception） |
| 实践 | 精确捕获 vs 裸 except、重试逻辑 |

⭐ **学习重点**
- **精确捕获 + 重试**：调 LLM API 必然遇到超时 / 限流，"捕获异常 → 重试 → 降级"是 Agent 开发的日常模式。
- **自定义异常**：给 Agent 工具定义业务异常，让失败可区分、可处理。

⚠️ 常见坑：裸 `except:` 吞掉一切错误导致难排查、finally 中的 return 覆盖结果。

---

### 07 文件 IO

| 类别 | 知识点 |
|------|--------|
| 文本文件 | open / read / write、with 打开、编码（utf-8） |
| 路径 | os.path 与 pathlib（Path 对象） |
| 结构化文件 | json 读写（json.load / dump / dumps / loads）、csv |
| 二进制 | rb / wb 模式初识 |

⭐ **学习重点**
- **json 读写**：Prompt 模板、配置文件、API 交互全是 json，必须熟练。
- **pathlib**：现代路径写法，RAG 加载文档目录必用。
- **csv 读取**：贴合你数据分析的本职工作。

⚠️ 常见坑：Windows 编码问题（记得 `encoding="utf-8"`）、忘用 with 导致文件不关闭。

---

### 08 模块与包

| 类别 | 知识点 |
|------|--------|
| 模块 | import、from...import、`__name__ == "__main__"` |
| 包 | `__init__.py`、包的层级组织 |
| 环境 | pip / uv 基础、requirements / pyproject.toml |
| 第三方库 | 安装、版本管理、虚拟环境（venv / uv） |

⭐ **学习重点**
- **`__name__ == "__main__"`**：脚本与模块双用的标准写法，LangServe 部署代码里就有。
- **虚拟环境与 uv**：你已在用，理解"为什么需要隔离"即可达标。
- **包结构组织**：为后面把自己的 Agent 项目拆成多文件做准备。

⚠️ 常见坑：循环导入、把脚本命名为标准库名（如 `json.py`）导致导入错乱。

---

## 第 3 层 · 工程能力（09-11）

### 09 标准库（挑 Agent 开发高频的学）

| 类别 | 知识点 | 优先级 |
|------|--------|--------|
| json / dataclasses / enum | 结构定义与序列化 | ⭐⭐⭐ |
| logging | 日志分级、格式化、FileHandler | ⭐⭐ |
| datetime / time | 时间处理、格式化 | ⭐⭐ |
| os / sys / pathlib | 环境变量、路径 | ⭐⭐ |
| collections | defaultdict、Counter、namedtuple | ⭐⭐ |
| re（正则） | 匹配、分组、替换 | ⭐⭐（RAG 数据清洗刚需） |

⭐ **学习重点**
- **环境变量**：`os.environ.get("API_KEY")` —— API Key 管理的第一课（配合 .env）。
- **logging**：Agent 调试不要只用 print，学会打结构化日志。
- **defaultdict / Counter**：统计类任务和状态管理好用。

---

### 10 并发编程（⭐ 结合 GIL 一起学）

| 类别 | 知识点 |
|------|--------|
| 概念 | 并发 vs 并行、IO 密集 vs CPU 密集 |
| 多线程 | threading、线程安全、锁 |
| 多进程 | multiprocessing、适用场景 |
| GIL | 是什么、为什么 IO 密集不受影响、面试标准答法 |

⭐ **学习重点**
- **GIL**：你计划中的重点。掌握"IO 密集用线程/异步、CPU 密集用多进程"这条选型逻辑。
- **并发选型思维**：为学 asyncio 铺路——理解了线程的局限，才懂 asyncio 的价值。

⚠️ 常见坑：以为开多线程就能加速 CPU 计算（GIL 限制）、锁的滥用导致死锁。

---

### 11 网络编程（重点花在 HTTP 层）

| 类别 | 知识点 | 优先级 |
|------|--------|--------|
| HTTP 基础 | 请求方法、状态码、Header、请求/响应体 | ⭐⭐⭐ |
| requests / httpx | GET / POST、超时、重试、Session | ⭐⭐⭐ |
| REST 概念 | 资源、端点、JSON API | ⭐⭐ |
| socket | TCP / UDP 原理 | ⭐（了解即可） |

⭐ **学习重点**
- **requests/httpx 调 API**：手动调一次 LLM 的 HTTP 接口（不借助 SDK），彻底理解"模型调用 = HTTP 请求"。
- **超时与重试**：生产 Agent 的稳定性来源。

⚠️ 常见坑：不设超时导致请求永久挂起、明文写死 API Key。

---

## 需要补充 · Agent 开发强依赖（12-15）

### 12 asyncio 异步编程（⭐⭐⭐ 最重要缺口）

| 类别 | 知识点 |
|------|--------|
| 核心 | async / await、协程函数与协程对象、事件循环 |
| 并发 | asyncio.gather、Task、create_task |
| 实战 | 异步 HTTP（httpx.AsyncClient）、异步生成器 |

⭐ **学习重点**
- **`astream` / `ainvoke` / `abatch`**：LangChain 异步接口全部基于 asyncio，不会异步就只能单线程傻等。
- **gather 并发调多个工具**：Agent 同时查 3 个数据源，异步比串行快数倍。
- 先理解"协程是可暂停的函数"，再上手写，不要死记语法。

---

### 13 typing 类型注解（⭐⭐⭐）

| 类别 | 知识点 |
|------|--------|
| 基础 | int / str / list[str] / dict[str, Any]、函数签名注解 |
| 进阶 | Optional、Union、Literal、Callable |
| 组合 | TypedDict、Generic、TypeVar 初识 |

⭐ **学习重点**
- **TypedDict**：LangGraph State 的定义方式，不会它就写不了 Graph。
- **Optional / Union**：Tool 参数与返回值签名随处可见。
- 注解不影响运行时，但框架靠它做校验与生成 Schema——理解这个"为什么"。

---

### 14 Pydantic 模型（⭐⭐⭐）

| 类别 | 知识点 |
|------|--------|
| 核心 | BaseModel、字段类型、默认值、Field |
| 校验 | 自动类型校验、validator、报错处理 |
| 序列化 | model_dump / model_dump_json、model_validate |
| 进阶 | 嵌套模型、配置管理（pydantic-settings + .env） |

⭐ **学习重点**
- **Structured Output**：让 LLM 按你的 Pydantic 模型吐结构化数据，Agent 输出可靠性的关键。
- **Tool 参数 Schema**：LangChain 自动把 Pydantic 模型转成工具描述给模型看。
- **pydantic-settings**：一石二鸟，同时解决环境变量管理（Git 密钥安全）。

---

### 15 HTTP 与 API 调用（⭐⭐）

> 若已并入 11 学过 requests，此处重点是**异步版 httpx + 流式响应**。

| 类别 | 知识点 |
|------|--------|
| 客户端 | httpx（同步 + 异步）、Session 复用 |
| 实战 | 调 LLM API、SSE 流式响应、Webhook |
| 工程化 | 超时、重试、错误码分类处理 |

⭐ **学习重点**
- 手写一次"裸调 OpenAI/DeepSeek 接口"：理解 messages、role、stream 参数的本质。
- SSE 流式响应的读取方式——就是"HTTP 版生成器"。

---

## 附 · 配套工程能力（与主轴并行，不占主线）

| 模块 | 必学内容 | 建议时机 |
|------|---------|---------|
| Git | add / commit / branch / push / pull、解决冲突 | 学到 08 时并行开始 |
| pytest | 断言、fixture 初识、给工具函数写测试 | 学完 06 后 |
| FastAPI | 路由、请求模型、部署服务 | ✅ 你已在学，保持 |
| Docker | 镜像、Dockerfile、运行容器 | 项目能跑通后再补 |

---

## 学习节奏建议（每周 6 天 × 2 小时）

| 阶段 | 模块 | 目标 |
|------|------|------|
| 第 1-4 周 | 01 → 04（含 OOP 进阶补丁） | 能读懂并写出类与继承 |
| 第 5-8 周 | 05 → 08 | 装饰器 / 生成器能独立写出来 |
| 第 9-11 周 | 09 → 11（含 re、SQLAlchemy） | 能手写脚本调 API、读写 json |
| 第 12-13 周 | 12 → 15（异步 / typing / Pydantic） | 接 LangChain 前的硬缺口全部补齐 |
| 之后 | LangChain / LangGraph 项目实战 | 你已在推进的 agents 链路 |

> 检验标准：每个模块学完，合上笔记能独立写一个 50 行以内的小程序用上该模块核心知识点，即为过关。
