from typing import Optional
import redis.asyncio as redis
from app.core.config import settings

# Global Redis client
redis_client: Optional[redis.Redis] = None


async def get_redis() -> redis.Redis:
    """
    Get Redis client instance.
    
    Returns:
        Redis client
    """
    global redis_client
    
    if redis_client is None:
        redis_client = redis.from_url(
            settings.redis_url,
            encoding="utf-8",
            decode_responses=True,
            max_connections=10,
        )
    
    return redis_client


async def close_redis() -> None:
    """Close Redis connection."""
    global redis_client
    
    if redis_client:
        await redis_client.close()
        redis_client = None
