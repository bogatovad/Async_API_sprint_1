from functools import lru_cache

from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.person import PersonDescription
from services.cache_backend import AsyncCacheStorage, cache
from services.data_storage import DataStorage


class PersonService:
    def __init__(self, cache_backend: AsyncCacheStorage, data_storage: DataStorage):
        self.cache_backend = cache_backend
        self.data_storage = data_storage

    @cache
    async def search_persons(self, *args, **kwargs):
        return await self.data_storage.search(*args, **kwargs)

    @cache
    async def get_film_by_id(self, *args, **kwargs):
        return await self.data_storage.get_persons_film_by_id(*args, **kwargs)

    @cache
    async def get_data_by_id(self, *args, **kwargs):
        data_for_person = await self.data_storage.get_by_id(*args, **kwargs)
        return PersonDescription(**data_for_person)


@lru_cache()
def get_person_service(
        cache_backend: AsyncCacheStorage = Depends(get_redis),
        elastic: DataStorage = Depends(get_elastic),
) -> PersonService:
    return PersonService(cache_backend, elastic)
