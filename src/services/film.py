import logging
import pickle
from functools import lru_cache

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from core.config import settings
from db.elastic import get_elastic
from db.redis import get_redis
from models.film import Film
from services.cache_backend import RedisCache
from services.paginator import Paginator
from services.utils import es_search_template

from typing import Callable, Optional

logger = logging.getLogger(__name__)

ResponseType = Optional[Film | list[Film]]


def cache(get_data_from_elastic: Callable[..., ResponseType]) -> Callable[..., ResponseType]:
    """Декоратор, осуществляющий кэширование запросов."""
    async def wrapper(self, *args, **kwargs):
        # Получили ключ.
        key = get_key(*args)
        film = await self.get_from_cache(key)

        if film is not None:
            return film

        film = await get_data_from_elastic(self, args, kwargs)

        # Сохранили данные в кэш.
        await self.set_to_cache(key, film, settings.FILM_CACHE_EXPIRE_IN_SECONDS)
        return film
    return wrapper


def get_key(*args, **kwargs) -> str:
    """Генерация ключа для redis."""
    print('sdfsdfsdf', args)
    params,  = args
    starlette_requests = params.get("request")
    return str(starlette_requests.url)


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

    async def get_films_alike(self, film_id: str):
        cache_key = f'films/alike/{film_id}'
        films = await self.redis.get(cache_key)
        if films:
            logger.debug(f'Getting info from cache by key {cache_key}')
            return pickle.loads(films)
        film = await self.get_by_id(film_id)
        genres = film.genre
        query_params = {
            "query": {
                "terms": {
                    "genre": genres
                }
            }
        }
        films = await self.elastic.search(index="movies", body=query_params)
        films = [Film(**film['_source']) for film in films['hits']['hits']]

        logger.debug(f'Storing info ini cache by key {cache_key}')
        await self.redis.set(cache_key, pickle.dumps(films), expire=settings.FILM_CACHE_EXPIRE_IN_SECONDS)

        return films

    @cache
    async def get_all_films(self, *args, **kwargs):
        print(f'DSSA!! {kwargs=}')
        page, body = es_search_template(self.index, *args)
        loads_films = await self.paginator(self.index, body, page)
        films_schema = [Film(**film['_source']) for film in loads_films]
        return films_schema

    async def get_search(self, query_params):
        page, body = es_search_template(self.index, query_params)
        data_for_key = self.preparation_data_for_key(self.index, query_params)
        key_movies_search = self.create_key(data_for_key)
        loads_movies = await self.get_from_cache(key_movies_search)

        if not loads_movies:
            loads_movies = await self.paginator(self.index, body, page)
            value = self.create_value(loads_movies)
            await self.set_to_cache(key_movies_search, value, settings.FILM_CACHE_EXPIRE_IN_SECONDS)
        return [Film(**movie['_source']) for movie in loads_movies]


@lru_cache()
def get_film_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)
