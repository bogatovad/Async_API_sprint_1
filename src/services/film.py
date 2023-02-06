import logging
from functools import lru_cache
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.film import Film
from services.cache_backend import AsyncCacheStorage, cache
from services.data_storage import DataStorage

logger = logging.getLogger(__name__)


class FilmService:
    def __init__(self, cache_backend: AsyncCacheStorage, data_storage: DataStorage):
        self.cache_backend = cache_backend
        self.data_storage = data_storage

    @cache
    async def get_data_by_id(self, *args, **kwargs) -> Film | None:
        film = await self.data_storage.get_by_id(*args)
        if not film:
            return None
        return film

    @cache
    async def get_films_alike(self, *args, **kwargs):
        return await self.data_storage.get_alike(*args, *kwargs)

    @cache
    async def get_all_films(self, *args, **kwargs):
        return await self.data_storage.get_list(*args, **kwargs)

    @cache
    async def get_search(self, *args, **kwargs):
        return await self.data_storage.search(*args, **kwargs)


@lru_cache()
def get_film_service(
        cache_backend: AsyncCacheStorage = Depends(get_redis),
        data_storage: DataStorage = Depends(get_elastic),
) -> FilmService:
    return FilmService(cache_backend, data_storage)
