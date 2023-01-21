import pickle
from abc import ABC


class CacheBackend(ABC):
    """Интерфейс для класса, реализующего методы кэширования."""

    def create_key(self, data):
        """Создание ключа."""
        pass

    def create_value(self, data):
        """Создание данных."""
        pass

    async def get_from_cache(self, key):
        """Получить данные из кэша."""
        pass

    async def set_to_cache(self, key, value, expire):
        """Положить данные в кэш."""
        pass


class RedisCache(CacheBackend):
    """Кэш, реализует логику кэширования для запросов с query и filter."""

    def create_key(self, data):
        return pickle.dumps(data)

    def create_value(self, data):
        return pickle.dumps(data)

    @staticmethod
    def preparation_data_for_key(index, data: dict):
        """Подготовка данных для генерации ключа."""
        data_copy = data.copy()
        data_copy["index"] = index
        return data_copy

    async def get_from_cache(self, key):
        get_from_cache = await self.redis.get(key)
        loads_objects_from_cache = None
        if get_from_cache:
            loads_objects_from_cache = pickle.loads(get_from_cache)
        return loads_objects_from_cache

    async def set_to_cache(self, key, value, expire):
        await self.redis.set(key, value, expire=expire)
