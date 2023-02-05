from functools import lru_cache

from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from services.cache_backend import AsyncCacheStorage, cache
from services.data_storage import AsyncElasticDataStorage


class GenreService(AsyncElasticDataStorage):
    def __init__(self, cache_backend: AsyncCacheStorage, elastic: AsyncElasticsearch):
        self.cache_backend = cache_backend
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
        cache_backend: AsyncCacheStorage = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(cache_backend, elastic)
