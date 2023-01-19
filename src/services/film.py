from functools import lru_cache
from typing import Optional, Union

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError

from db.elastic import get_elastic
from db.redis import get_redis
from fastapi import Depends
from models.services.film import Film
from models.services.genre import GenreId
from services.paginator import Paginator

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5


class FilmService(Paginator):
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_by_id(self, film_id: str) -> Optional[Film]:
        film = await self._film_from_cache(film_id)
        if not film:
            film = await self._get_film_from_elastic(film_id)
            if not film:
                return None
            await self._put_film_to_cache(film)

        return film

    async def get_all(self):
        ...

    async def _get_film_from_elastic(self, film_id: str) -> Optional[Film]:
        try:
            doc = await self.elastic.get('movies', film_id)
        except NotFoundError:
            return None
        doc = doc['_source']
        return Film(**doc)

    async def _film_from_cache(self, film_id: str) -> Optional[Film]:
        data = await self.redis.get(film_id)
        if not data:
            return None
        film = Film.parse_raw(data)
        return film

    async def _put_film_to_cache(self, film: Film):
        await self.redis.set(film.id, film.json(), expire=FILM_CACHE_EXPIRE_IN_SECONDS)

    async def get_all_films(self, sort: str, page: int, size: int, filter: Union[str, None]):
        query = {}

        if filter:
            genre = await self.elastic.get("genres", filter)
            genre_schema = GenreId(**genre['_source'])
            query["query"] = {
                "match": {
                    "genre": genre_schema.name
                }
            }
        else:
            query["query"] = {
                "match_all": {}
            }
        order_sort = "desc" if sort[0] == '-' else "asc"
        query_params = {
            **query,
            "sort": {
                "imdb_rating": {
                    "order": order_sort
                }
            },
            "size": f"{size}",
        }

        films = await self.paginator("movies", query_params, page)
        films_schema = [Film(**film['_source']) for film in films]
        return films_schema


@lru_cache()
def get_film_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)
