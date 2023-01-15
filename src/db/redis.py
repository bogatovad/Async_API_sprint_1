from aioredis import Redis

redis: Redis | None = None


async def get_redis() -> Redis:
    """Функция для внедрения зависимостей."""
    print(redis)
    return redis
