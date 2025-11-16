"""Redis connection management"""

import redis.asyncio as redis
from typing import AsyncGenerator

from .config import settings

# Create Redis connection pool
redis_pool = None


async def get_redis_pool():
    """Get or create Redis connection pool"""
    global redis_pool
    if redis_pool is None:
        redis_pool = redis.ConnectionPool.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True,
            max_connections=50,
        )
    return redis_pool


async def get_redis() -> AsyncGenerator[redis.Redis, None]:
    """Get Redis client"""
    pool = await get_redis_pool()
    client = redis.Redis(connection_pool=pool)
    try:
        yield client
    finally:
        await client.close()


async def close_redis_pool():
    """Close Redis connection pool"""
    global redis_pool
    if redis_pool is not None:
        await redis_pool.disconnect()
        redis_pool = None
