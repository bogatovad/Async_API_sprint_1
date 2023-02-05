from abc import ABC, abstractmethod
from typing import Callable
from models.film import Film
from core.config import settings
from models.film import Film
from services.serializer import PickleSerializeData

ResponseType = Film | list[Film] | None


class CacheBackend(ABC):
    """Интерфейс для класса, реализующего методы кэширования."""

    async def get_from_cache(self, key):
        """Получить данные из кэша."""
        pass

    async def set_to_cache(self, key, value, expire):
        """Положить данные в кэш."""
        pass


class AsyncCacheStorage(ABC):
    @abstractmethod
    async def get(self, key: str, **kwargs):
        pass

    @abstractmethod
    async def set(self, key: str, value: str, expire: int, **kwargs):
        pass


class RedisCache(CacheBackend, PickleSerializeData):
    """Кэш, реализует логику кэширования для запросов с query и filter."""

    async def get_from_cache(self, key):
        data_from_cache = await self.redis.get(key)
        if data_from_cache:
            return self.deserialize(data_from_cache)

    async def set_to_cache(self, key, value, expire):
        value = self.serialize(value)
        await self.redis.set(key, value, expire=expire)


def get_key(*args, **kwargs) -> str:
    """Генерация ключа для redis."""
    params,  = args
    starlette_requests = params.get("request")
    return str(starlette_requests.url)


def cache(get_data_from_elastic: Callable[..., ResponseType]) -> Callable[..., ResponseType]:
    """Декоратор, осуществляющий кэширование запросов."""
    async def wrapper(self, *args, **kwargs):
        # Получили ключ.
        key = get_key(*args)
        data = await self.get_from_cache(key)

        if data is not None:
            return data

        data = await get_data_from_elastic(self, args, kwargs)

        # Сохранили данные в кэш.
        await self.set_to_cache(key, data, settings.film_cache_expire_in_seconds)
        return data
    return wrapper
