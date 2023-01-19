from functools import lru_cache

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError

from db.elastic import get_elastic
from db.redis import get_redis
from fastapi import Depends
from models.services.genre import GenreId


class GenreService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_by_id(self, genre_id: str):
        genre = await self.elastic.get("genres", genre_id)
        genre_schema = GenreId(**genre['_source'])
        return genre_schema

    async def get_list(self):
        try:
            docs = await self.elastic.search(index="genres", body={"query": {"match_all": {}}})
            genres = docs['hits']['hits']
            genres_schema = [GenreId(**genre['_source']) for genre in genres]
        except NotFoundError:
            return None
        return genres_schema


@lru_cache()
def get_genre_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis, elastic)
