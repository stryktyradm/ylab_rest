import json
from typing import Any

from aioredis import Redis
from src.core.config import settings


class BaseCacheRepository:
    def __init__(self, cache: Redis):
        self.cache = cache

    async def get(self, key: str):
        cache_data = await self.cache.get(key)
        if cache_data:
            return json.loads(cache_data)

    async def add(self, key: str, value: Any):
        value = json.dumps(value)
        await self.cache.set(key, value, ex=settings.REDIS_CACHE_TIME)

    async def clear(self, key: str):
        await self.cache.delete(key)

    async def multi_clear(self, pattern: str, root: str):
        keys = await self.cache.keys(pattern)
        await self.cache.delete(*keys, root)
