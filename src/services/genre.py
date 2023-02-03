from functools import lru_cache

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.genre import Genre
from services.cache_backend import cache, RedisCache


class GenreService(RedisCache):
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    @cache
    async def get_by_id(self, *args, **kwargs):
        return await self._get_genre_from_elastic(*args)

    async def _get_genre_from_elastic(self, *args, **kwargs) -> Genre | None:
        params, _ = args
        try:
            doc = await self.elastic.get('genres', params[0].get("genre_id"))
        except NotFoundError:
            return None
        doc = doc['_source']
        return Genre(**doc)

    @cache
    async def get_list(self, *args, **kwargs):
        return await self._get_genre_list_from_elastic()

    async def _get_genre_list_from_elastic(self) -> list[Genre] | None:
        try:
            docs = await self.elastic.search(index="genres", body={"query": {"match_all": {}}})
        except NotFoundError:
            return []
        return [Genre(**genre['_source']) for genre in docs['hits']['hits']]


@lru_cache()
def get_genre_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis, elastic)
