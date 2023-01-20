import pickle
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

    async def get_all_films(self, sort: str, page: int, size: int, _filter: Union[str, None]):
        query = {}
        # todo: фильтрация может быть только по жанру или есть другие варианты?
        # todo: также стоит разнести логику метода и преобразование к http формату данных.
        if _filter:
            genre = await self.elastic.get("genres", _filter)
            genre_schema = GenreId(**genre['_source'])
            query["query"] = dict(match={
                "genre": genre_schema.name
            })
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

        query_params_copy = query_params.copy()
        query_params_copy["index"] = "movies"
        key_list_movies = pickle.dumps(query_params_copy)
        films = await self.redis.get(key_list_movies)
        if films:
            return pickle.loads(films)
        films = await self.paginator("movies", query_params, page)
        films_schema = [Film(**film['_source']) for film in films]
        await self.redis.set(key_list_movies, pickle.dumps(films_schema))
        return films_schema


@lru_cache()
def get_film_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)
