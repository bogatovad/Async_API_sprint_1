from functools import lru_cache
from typing import Optional

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError

from db.elastic import get_elastic
from db.redis import get_redis
from fastapi import Depends
from models.services.film import Film
from .base_service import BaseService


class FilmService(BaseService):
    pass


    async def get_by_params(self, params):
        films_list = await self._get_from_cache()
        if not films_list:
            films_list = await self._get_films_from_elastic()

    async def _get_films_from_elastic(self, film_id: str) -> Optional[Film]:
        films_list = await self.elastic.search(
            index="documents",
            body={"query": {"match_all": {}}},
            size=20,
        )


@lru_cache()
def get_film_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic, 'movies', Film)
