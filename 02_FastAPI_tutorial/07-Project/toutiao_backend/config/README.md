
## 数据库
- 数据库配置：/config/
- 数据模型层: /models/ （SQLAlchemy ORM）
- 数据操作层: /crud/ 

## MySQL
### 1. 建库
database.sql (Pycharm -> 右键 localhost -> SQL脚本 -> 运行SQL脚本)

### 2. 配置 ORM
安装
```
# aiomysql-异步数据库驱动
uv add sqlalchemy[asyncio] aiomysql 
```
建表（由于步骤 1 已经建表，下面2和3可以省略）
1. `create_async_engine` 创建异步引擎
2. 定义模型基类（继承 `DeclarativeBase`）和模型类
3. `run_sync(Base.metadata.create_all)`建表

### 3. 操作数据
1. 路由处理函数注入数据库会话依赖项 Depends
2. 查询数据：select()
3. 增加数据：add()
4. 更新数据：重新赋值
5. 删除数据：delete()

## Redis
- 高性能的 `Key-Value 存储系统`
- 数据存储在`内存`中，因此读写速度极快

缓存、击穿、雪崩、穿透、数据一致性

### 1. 本地安装 Redis 服务端
- 下载 Redis 安装包并解压
- 运行 Redis 服务端：`redis-server.exe`

### 2. 配置 Redis 客户端
安装
```
uv add redis
```

配置 Redis 客户端
```
import redis.asyncio as redis
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
```

### 3. 封装缓存操作
缓存操作就是围绕 Redis 做 "存、取、删、判断、过期"等操作

Redis 存储数据：Key-Value

| 方法 | 参数 | 描述 |
| :--- | :--- | :--- |
| `setex` | `key: str`,<br>`expire: int（秒）`,<br>`value: str` | 设置缓存并指定过期时间（秒） |
| `get` | `key: str` | 获取缓存值。若缓存不存在，返回 `None` |
| `delete` | `key: str` | 删除指定的缓存键 |
| `exists` | `key: str` | 检查缓存键是否存在，返回布尔值 |

### 4. 设计缓存策略
最常见的策略 - 旁路策略
- 读：先查缓存，有数据则返回，没有数据则查询数据库
- 写：更新数据库后，更新或删除缓存数据