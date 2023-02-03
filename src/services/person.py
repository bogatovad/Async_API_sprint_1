from functools import lru_cache

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.film import FilmShort
from models.person import PersonDescription
from services.cache_backend import RedisCache, cache
from services.paginator import Paginator
from services.utils import es_search_template


class PersonService(Paginator, RedisCache):
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic
        self.index = "persons"

    @cache
    async def search_persons(self, *args, **kwargs):
        page, body = es_search_template(self.index, *args)
        loads_persons = await self.paginator(self.index, body, page)
        params, _ = args
        return [
            await self.get_by_id(
                dict(
                    person_id=person['_source']['id'],
                    request=params[0].get('request')
                )
            )
            for person in loads_persons
        ]

    async def get_film_by_id(self, person_id: str):
        body = {
            "query": {
                "nested": {
                    "path": "actors",
                    "query": {
                        "match": {
                            "actors.id": f"{person_id}"
                        }
                    }
                }
            }
        }
        docs_actors = await self.elastic.search(index="movies", body=body)
        return [FilmShort(**movie['_source']) for movie in docs_actors['hits']['hits']]

    async def _get_movies_actors(self, person_id: str):
        person = await self.elastic.get("persons", person_id)
        body_actor = {
            "query": {
                "nested": {
                    "path": "actors",
                    "query": {
                        "match": {
                            "actors.id": f"{person_id}"
                        }
                    }
                }
            }
        }
        docs_actors = await self.elastic.search(index="movies", body=body_actor)
        count_movies_actor = docs_actors['hits']['total']['value']
        movies_actor = [movie['_source']['id'] for movie in docs_actors['hits']['hits']]
        return person, count_movies_actor, movies_actor

    async def _get_movies_writers(self, person_id: str):
        body_writer = {
            "query": {
                "nested": {
                    "path": "writers",
                    "query": {
                        "match": {
                            "writers.id": f"{person_id}"
                        }
                    }
                }
            }
        }
        docs_writes = await self.elastic.search(index="movies", body=body_writer)
        count_movies_writers = docs_writes['hits']['total']['value']
        movies_writer = [movie['_source']['id'] for movie in docs_writes['hits']['hits']]
        return count_movies_writers, movies_writer

    async def _get_movies_directors(self, full_name: str):
        body_director = {
            "query": {
                "match": {
                    "director": f"{full_name}"
                }
            }
        }
        docs_director = await self.elastic.search(index="movies", body=body_director)
        count_movies_director = docs_director['hits']['total']['value']
        movies_director = [movie['_source']['id'] for movie in docs_director['hits']['hits']]
        return count_movies_director, movies_director

    async def _get_actors_from_cache_or_elastic(self, *args, **kwargs):
        params, _ = args
        return await self._get_movies_actors(params[0].get('person_id'))

    async def _get_writers_from_cache_or_elastic(self, *args, **kwargs):
        params, _ = args
        return await self._get_movies_writers(params[0].get('person_id'))

    async def _get_directors_from_cache_or_elastic(self, full_name: str):
        return await self._get_movies_directors(full_name)

    @cache
    async def get_by_id(self, *args, **kwargs):
        person, count_movies_actor, movies_actor = await self._get_actors_from_cache_or_elastic(*args)
        count_movies_writers, movies_writer = await self._get_writers_from_cache_or_elastic(*args)
        full_name = person['_source']['full_name']
        count_movies_director, movies_director = await self._get_directors_from_cache_or_elastic(full_name)
        film_ids = list(set(movies_actor + movies_writer + movies_director))
        role = [
            role[0] for role in (
                ('actor', count_movies_actor),
                ('writer', count_movies_writers),
                ('director', count_movies_director)
            ) if role[1] != 0
        ]
        return PersonDescription(**person['_source'], role=role, film_ids=film_ids)


@lru_cache()
def get_person_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(redis, elastic)
