from fastapi import Request, HTTPException, status
from redis.asyncio import Redis
from app.config import settings
from datetime import datetime, timezone

redis_client = Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    encoding="utf-8",
    decode_responses=True
)

class RedisRateLimiter:
    def __init__(self, expire: int = settings.REDIS_EXPIRE_SECONDS, limit: int = settings.REDIS_LIMIT):
        self.expire = expire
        self.limit = limit

    async def __call__(self, request: Request):
        current_minute = int(datetime.now(timezone.utc).timestamp() // 60)
        client_ip = request.headers.get("X-Forwarded-For").split(",")[0].strip()
        current_usage = await redis_client.incr(f"rate:{client_ip}:{current_minute}")

        if current_usage == 1:
            await redis_client.expire(f"rate:{client_ip}:{current_minute}", self.expire)

        if current_usage > self.limit:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many requests"
            )