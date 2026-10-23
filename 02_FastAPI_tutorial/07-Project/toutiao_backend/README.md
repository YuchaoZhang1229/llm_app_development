# AI掘金头条新闻系统(Toutiao News)

一个基于FastAPI和SQLAlchemy构建的现代化新闻系统，支持用户注册登录、新闻浏览、收藏和历史
记录等功能。

## 1-2 项目概述
这是一个仿今日头条的新闻系统后端API服务，采用异步Python框架FastAPI开发，使用MySQL作为数据
库存储，通过SQLAIchemyORM进行数据访问。系统提供完整的用户管理、新闻浏览、收藏和历史记录
功能。

## 1-2 技术栈
- 后端框架：FastAPI
- 数据库：MySQL
- ORM：SQLAlchemy（异步）
- 数据库驱动：aiomysql
- 密码加密：passlib + bcrypt
- 缓存系统：Redis
- 异步支持：Python asyncio

## 1-3 项目结构
```
toutiao backend/      # 项目
|————crud/            # 数据访问层（CRUD操作）
|    |————users.py          # 用户相关数据库操作
|    |————news.py           # 新闻相关数据库操作
|
|————models/          # 数据库模型（SQLAlchemy ORM）
|    |————users.py          # 用户相关数据模型
|    |————news.py           # 新闻相关数据模型
|
|————routers/         # 路由层（按模块划分）
|    |————users.py          # 用户相关路由
|    |————news.py           # 新闻相关路由
|
|————schemas/         # 数据验证模型（Pydantic模型）
|    |————users.py          # 用户相关数据验证模型
|    |————news.py           # 新闻相关数据验证模型
|
|————utils/           # 工具函数
|
|————config/          # 配置文件
|     |————db_conf.py      # 数据库配置
|     |————redis_conf.py   # Redis配置
|
|————main.py          # 主程序入口：创建app、挂载路由、中间件
|————test_main.http   # HTTP接口测试文件
```

## 1-4 功能模块
### 1. 用户管理模块
- 用户注册
- 用户登录
- 用户信息获取
- 用户信息更新
- 用户密码修改

### 2. 缓存模块
- 用户历史记录缓存

## 1-5 数据库设计
### 主要数据表
1. 用户表（user）
- 用户基本信息存储
- 包含用户名、密码（加密）、昵称、头像等字段

2. 用户令牌表（user_token）
- 用户认证令牌管理
- 支持令牌过期机制

## 1-6 缓存设计
### 缓存策略
系统采用Redi作为缓存层，对高频访问的数据进行缓存，以提升系统性能和响应速度。

### 缓存数据类型


### 缓存配置
在 redis——conf.py 中配置 Redis 连接信息：
```
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0
```

## 1-7 API接口说明

### 用相关接口
| 接口 | 方法 | 说明 |
| :--- | :---: | :--- |
| `/api/user/register` | POST | 用户注册 |
| `/api/user/login` | POST | 用户登录 |
| `/api/user/info` | GET | 获取用户信息 |
| `/api/user/update` | PUT | 更新用户信息 |
| `/api/user/password` | PUT | 修改用户密码 |

## 1-8 认证机制
系统使用基于令牌（Token）的认证机制：
1. 用户登录成功后返回访问令牌
2. 需要认证的接口在请求头中添加`Authorization:token`值
3. 令牌有效期为7天

## 1-9 错误处理
系统提供统一的错误处理机制
- 用户认证失败返回401状态码
- 资源不存在返回404状态码
- 服务器内部错误返回500状态码

## 1-10 开发规范
- 使用异步数据库操作
- 所有密码均加密存储
- 接口返回统一的 JSON 格式
- 详细的接口文档和示例
- 缓存操作封装成独立函数便于调用

## 1-11 性能优化
- 使用 Redis 缓存热点数据 
- 异步数据库操作提升并发性能 
- 合理的数据库索引设计 
- 连接池管理减少连接开销