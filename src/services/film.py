from functools import lru_cache
from typing import Optional

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError

from db.elastic import get_elastic
from db.redis import get_redis
from fastapi import Depends
from models.services.film import Film
from services.cache_backend import RedisCache
from services.paginator import Paginator
from services.utils import es_search_template

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5


class FilmService(Paginator, RedisCache):
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic
        self.index = "movies"

    async def get_by_id(self, film_id: str) -> Optional[Film]:
        film = await self._film_from_cache(film_id)
        if not film:
            film = await self._get_film_from_elastic(film_id)
            if not film:
                return None
            await self._put_film_to_cache(film)

        return film

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

    async def get_all_films(self, query_params):
        page, body = es_search_template(self.index, query_params)
        data_for_key = self.preparation_data_for_key(self.index, query_params)
        key_list_movies = self.create_key(data_for_key)
        loads_films = await self.get_from_cache(key_list_movies)
        if loads_films is not None:
            return loads_films
        loads_films = await self.paginator(self.index, body, page)
        films_schema = [Film(**film['_source']) for film in loads_films]
        value = self.create_value(films_schema)
        await self.set_from_cache(key_list_movies, value, FILM_CACHE_EXPIRE_IN_SECONDS)
        return films_schema

    async def get_search(self, query_params):
        page, body = es_search_template(self.index, query_params)
        data_for_key = self.preparation_data_for_key(self.index, query_params)
        key_movies_search = self.create_key(data_for_key)
        loads_movies = await self.get_from_cache(key_movies_search)

        if not loads_movies:
            loads_movies = await self.paginator(self.index, body, page)
            value = self.create_value(loads_movies)
            await self.set_from_cache(key_movies_search, value, FILM_CACHE_EXPIRE_IN_SECONDS)
        return [Film(**movie['_source']) for movie in loads_movies]


@lru_cache()
def get_film_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)
