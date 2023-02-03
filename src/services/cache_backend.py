import pickle
from abc import ABC


class SerializeData(ABC):
    def serialize(self, data):
        """Сериализация данных."""
        pass

    def deserialize(self, data):
        """Распаковка данных."""
        pass


class PickleSerializeData(SerializeData):
    def serialize(self, data):
        return pickle.dumps(data)

    def deserialize(self, data):
        return pickle.loads(data)


class CacheBackend(ABC):
    """Интерфейс для класса, реализующего методы кэширования."""

    async def get_from_cache(self, key):
        """Получить данные из кэша."""
        pass

    async def set_to_cache(self, key, value, expire):
        """Положить данные в кэш."""
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
