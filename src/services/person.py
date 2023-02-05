from functools import lru_cache

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.person import PersonDescription
from services.cache_backend import RedisCache, cache, AsyncCacheStorage
from services.data_storage import AsyncElasticDataStorage
from services.paginator import Paginator


class PersonService(Paginator, RedisCache, AsyncElasticDataStorage):
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic
        self.index = "persons"

    @cache
    async def search_persons(self, *args, **kwargs):
        return await self.search(*args, **kwargs)

    @cache
    async def get_film_by_id(self, *args, **kwargs):
        return await self.get_persons_film_by_id(*args, **kwargs)

    @cache
    async def get_data_by_id(self, *args, **kwargs):
        data_for_person = await self.get_by_id(*args, **kwargs)
        return PersonDescription(**data_for_person)


@lru_cache()
def get_person_service(
        cache: AsyncCacheStorage = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(cache, elastic)
