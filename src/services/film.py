import logging
from functools import lru_cache

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError

from db.elastic import get_elastic
from db.redis import get_redis
from fastapi import Depends
from models.film import Film
from services.cache_backend import RedisCache, cache, AsyncCacheStorage
from services.paginator import Paginator
from services.utils import es_search_template

logger = logging.getLogger(__name__)


class FilmService(Paginator, RedisCache):
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic
        self.index = "movies"

    @cache
    async def get_by_id(self, *args, **kwargs) -> Film | None:
        film = await self._get_film_from_elastic(*args)
        if not film:
            return None
        return film

    async def _get_film_from_elastic(self, *args, **kwargs) -> Film | None:
        try:
            params, _ = args
            film_id: str = params[0].get('film_id')
            doc = await self.elastic.get('movies', film_id)
        except NotFoundError:
            return None
        doc = doc['_source']
        return Film(**doc)

    @cache
    async def get_films_alike(self, *args, **kwargs):
        params, _ = args
        film = await self.get_by_id(dict(
            film_id=params[0].get('film_id'),
            request=params[0].get('request')
        ))
        genres = film.genre

        # Запрос на поиск фильмов с таким же жанром.
        query_params = {
            "query": {
                "terms": {
                    "genre": genres
                }
            }
        }
        films = await self.elastic.search(index="movies", body=query_params)
        return [Film(**film['_source']) for film in films['hits']['hits']]

    @cache
    async def get_all_films(self, *args, **kwargs):
        page, body = es_search_template(self.index, *args)
        loads_films = await self.paginator(self.index, body, page)
        films_schema = [Film(**film['_source']) for film in loads_films]
        return films_schema

    @cache
    async def get_search(self, *args, **kwargs):
        page, body = es_search_template(self.index, *args)
        loads_movies = await self.paginator(self.index, body, page)
        return [Film(**movie['_source']) for movie in loads_movies]


@lru_cache()
def get_film_service(
        cache: AsyncCacheStorage = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(cache, elastic)
