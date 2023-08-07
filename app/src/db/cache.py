import aioredis
from aioredis import Redis
from src.core.config import settings


async def get_cache_connection() -> Redis:
    redis = await aioredis.from_url(url=settings.REDIS_URI)
    return redis
