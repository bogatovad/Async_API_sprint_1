from aioredis import Redis


redis: Redis | None

async def get_redis() -> Redis:
    """Функция для внедрения зависимостей."""
    return redis
