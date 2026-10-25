import json
from typing import Any
import redis.asyncio as redis

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0

# 创建 Redis 客户端
redis_client = redis.Redis(
    host=REDIS_HOST,        # Redis 服务器的主机地址
    port=REDIS_PORT,        # Redis 端口号
    db=REDIS_DB,            # Redis 数据库编号, 0-15
    decode_responses=True   # 是否将字节数据自动解码为字符串
)

# 读取：字符串
async def get_cache(key: str):
    try:
        return await redis_client.get(key)
    except Exception as e:
        print(f"获取缓存失败：{e}")
        return None


# 读取：列表[]或字典{}
async def get_json_cache(key: str):
    try:
        data = await redis_client.get(key)
        if data:
            return json.loads(data)  # 序列化
        return None
    except Exception as e:
        print(f"获取 JSON 缓存失败：{e}")
        return None


# 设置缓存 setex(key, expire, value)
async def set_cache(key: str, value: Any, expire: int = 3600):
    try:
        if isinstance(value, (dict, list)):
            # 转字符串再存
            value = json.dumps(value, ensure_ascii=False)  # 中文正常保存
        await redis_client.setex(key, expire, value)
        return True
    except Exception as e:
        print(f"设置缓存失败：{e}")
        return False


"""
=== 1. 字符串缓存测试 ===
输入: set_cache('user_name', '张三', 60)
输出: get_cache('user_name') -> 张三

=== 2. 字典(JSON)缓存测试 ===
输入: set_cache('user_info_101', {'id': 101, 'role': 'admin', 'status': True}, 3600)
输出: get_json_cache('user_info_101') -> {'id': 101, 'role': 'admin', 'status': True}
数据类型: <class 'dict'>

=== 3. 列表(JSON)缓存测试 ===
输入: set_cache('hot_tags', ['Python', 'Redis', '异步编程'], 1800)
输出: get_json_cache('hot_tags') -> ['Python', 'Redis', '异步编程']
数据类型: <class 'list'>

=== 4. 读取不存在的 Key ===
输出: get_cache('not_exist_key') -> None
"""