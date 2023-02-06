from abc import ABC, abstractmethod
from typing import Callable

from core.config import settings
from models.film import Film
from services.serializer import PickleSerializeData

ResponseType = Film | list[Film] | None


class AsyncCacheStorage(ABC):
    """Интерфейс для класса, реализующего методы кэширования."""

    @abstractmethod
    async def get(self, key: str, **kwargs):
        """Получить данные из кэша."""
        pass

    @abstractmethod
    async def set(self, key: str, value: str, expire: int, **kwargs):
        """Положить данные в кэш."""
        pass


def get_key(*args, **kwargs) -> str:
    """Генерация ключа для redis."""
    params,  = args
    starlette_requests = params.get("request")
    return str(starlette_requests.url)


def cache(get_data_from_elastic: Callable[..., ResponseType]) -> Callable[..., ResponseType]:
    """Декоратор, осуществляющий кэширование запросов."""
    async def wrapper(self, *args, **kwargs):
        serializer = PickleSerializeData()

        # Получили ключ.
        key = get_key(*args)

        data = await self.cache_backend.get(key)

        if data is not None:
            return serializer.deserialize(data)

        data = await get_data_from_elastic(self, *args, **kwargs)

        # Сохранили данные в кэш.
        await self.cache_backend.set(key, serializer.serialize(data), expire=settings.film_cache_expire_in_seconds)
        return data
    return wrapper
