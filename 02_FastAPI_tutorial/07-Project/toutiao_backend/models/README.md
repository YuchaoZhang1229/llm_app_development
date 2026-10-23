## 数据库模型层（SQLAlchemy ORM）
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