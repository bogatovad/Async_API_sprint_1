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

    async def get_all_films(self, query_params):
        query_params = {
            "query": {
            "match_all": {}
            }
        }
        doc = await self.elastic.search(
            index=self.index,
            body=query_params
        )
        return doc


@lru_cache()
def get_film_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic, 'movies', Film)
