import logging
from functools import lru_cache

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.film import Film
from services.cache_backend import RedisCache, cache, AsyncCacheStorage
from services.data_storage import AsyncElasticDataStorage
from services.paginator import Paginator

logger = logging.getLogger(__name__)


class FilmService(Paginator, RedisCache, AsyncElasticDataStorage):
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic
        self.index = "movies"

    @cache
    async def get_data_by_id(self, *args, **kwargs) -> Film | None:
        film = await self.get_by_id(*args)
        if not film:
            return None
        return film

    @cache
    async def get_films_alike(self, *args, **kwargs):
        return await self.get_alike(*args, *kwargs)

    @cache
    async def get_all_films(self, *args, **kwargs):
        return await self.get_list(*args, **kwargs)

    @cache
    async def get_search(self, *args, **kwargs):
        return await self.search(*args, **kwargs)


@lru_cache()
def get_film_service(
        cache: AsyncCacheStorage = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(cache, elastic)
