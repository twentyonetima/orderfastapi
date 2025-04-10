from redis.asyncio import Redis
from config import REDIS_HOST, REDIS_PORT

redis_client = Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

async def get_redis() -> Redis:
    return redis_client