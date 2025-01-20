import redis
import pymysql  # 数据库操作库

# 初始化 Redis 客户端
redis_client = redis.StrictRedis(
    host='redis-11331.c253.us-central1-1.gce.redns.redis-cloud.com',
    port=11331,  # 修改为实际端口
    password='your_redis_password',  # 如果有密码，填写这里
    decode_responses=True
)

# 从缓存或数据库中获取数据
def get_data(key, query_func):
    # 查询 Redis 缓存
    cached_data = redis_client.get(key)
    if cached_data:
        print("Cache hit")
        return eval(cached_data)  # 从 Redis 返回的数据需解析为 Python 对象
    
    print("Cache miss")
    # 缓存未命中，从数据库查询
    db_data = query_func()
    if db_data:
        # 写入缓存，设置过期时间
        redis_client.set(key, str(db_data), ex=300)
    return db_data

# 清除缓存
def clear_cache(key):
    redis_client.delete(key)
    print(f"Cache with key '{key}' has been cleared.")
