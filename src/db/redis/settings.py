import aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend


async def start_redis():
    redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

