from functools import lru_cache

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from services.cache_backend import RedisCache, cache, AsyncCacheStorage
from services.data_storage import AsyncElasticDataStorage


class GenreService(RedisCache, AsyncElasticDataStorage):
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic
        self.index = 'genres'

    @cache
    async def get_data_by_id(self, *args, **kwargs):
        return await self.get_by_id(*args, **kwargs)

    @cache
    async def get_data_list(self, *args, **kwargs):
        return await self.get_list(*args, **kwargs)


@lru_cache()
def get_genre_service(
        cache: AsyncCacheStorage = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(cache, elastic)
