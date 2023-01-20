import pickle
from functools import lru_cache
from typing import List, Optional

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError

from db.elastic import get_elastic
from db.redis import get_redis
from fastapi import Depends
from models.services.genre import GenreId

GENRE_CACHE_EXPIRE_IN_SECONDS = 60 * 5


class GenreService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_by_id(self, genre_id: str):
        genre = await self._genre_from_cache(genre_id)
        if not genre:
            genre = await self._get_genre_from_elastic(genre_id)
            if not genre:
                return []
            await self._put_genre_to_cache(genre)
        return genre

    async def _get_genre_from_elastic(self, genre_id: str) -> Optional[GenreId]:
        try:
            doc = await self.elastic.get('genres', genre_id)
        except NotFoundError:
            return None
        doc = doc['_source']
        return GenreId(**doc)

    async def _genre_from_cache(self, genre_id: str):
        data = await self.redis.get(genre_id)
        if not data:
            return None
        genre = GenreId.parse_raw(data)
        return genre

    async def _put_genre_to_cache(self, genre: GenreId):
        await self.redis.set(genre.id, genre.json(), expire=GENRE_CACHE_EXPIRE_IN_SECONDS)

    async def get_list(self):
        key_list_genres = "list_genres"
        genres = await self.redis.get(key_list_genres)
        if genres:
            return pickle.loads(genres)
        genres = await self._get_genre_list_from_elastic()
        if not genres:
            return []
        await self.redis.set(key_list_genres, pickle.dumps(genres), expire=GENRE_CACHE_EXPIRE_IN_SECONDS)
        return genres

    async def _get_genre_list_from_elastic(self) -> Optional[List[GenreId]]:
        try:
            docs = await self.elastic.search(index="genres", body={"query": {"match_all": {}}})
        except NotFoundError:
            return []
        return [GenreId(**genre['_source']) for genre in docs['hits']['hits']]


@lru_cache()
def get_genre_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis, elastic)
