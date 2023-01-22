import pickle
from functools import lru_cache

from aioredis import Redis
from elasticsearch import AsyncElasticsearch

from core.config import PERSON_CACHE_EXPIRE_IN_SECONDS
from db.elastic import get_elastic
from db.redis import get_redis
from fastapi import Depends
from models.services.film import FilmShort
from models.services.person import PersonDescription
from services.cache_backend import RedisCache
from services.paginator import Paginator
from services.utils import es_search_template


class PersonService(Paginator, RedisCache):
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic
        self.index = "persons"

    async def search_persons(self, query_params):
        page, body = es_search_template(self.index, query_params)
        data_for_key = self.preparation_data_for_key(self.index, query_params)
        key_person_search = self.create_key(data_for_key)
        loads_persons = await self.get_from_cache(key_person_search)
        if not loads_persons:
            loads_persons = await self.paginator(self.index, body, page)
            value = self.create_value(loads_persons)
            await self.set_to_cache(key_person_search, value, PERSON_CACHE_EXPIRE_IN_SECONDS)
        return [await self.get_by_id(person['_source']['id']) for person in loads_persons]

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

    async def _get_actors_from_cache_or_elastic(self, person_id: str):
        key_movies_actors = f"movies_actors_{person_id}"
        data_movies_actors = await self.redis.get(key_movies_actors)
        if data_movies_actors:
            person, count_movies_actor, movies_actor = pickle.loads(data_movies_actors)
        else:
            person, count_movies_actor, movies_actor = await self._get_movies_actors(person_id)
            await self.redis.set(key_movies_actors, pickle.dumps([person, count_movies_actor, movies_actor]),
                                 expire=PERSON_CACHE_EXPIRE_IN_SECONDS)
        return person, count_movies_actor, movies_actor

    async def _get_writers_from_cache_or_elastic(self, person_id: str):
        key_movies_writers = f"movies_writers_{person_id}"
        data_movies_writers = await self.redis.get(key_movies_writers)
        if data_movies_writers:
            count_movies_writers, movies_writer = pickle.loads(data_movies_writers)
        else:
            count_movies_writers, movies_writer = await self._get_movies_writers(person_id)
            await self.redis.set(key_movies_writers, pickle.dumps([count_movies_writers, movies_writer]),
                                 expire=PERSON_CACHE_EXPIRE_IN_SECONDS)
        return count_movies_writers, movies_writer

    async def _get_directors_from_cache_or_elastic(self, person_id: str, full_name: str):
        key_movies_directors = f"movies_directors_{person_id}"
        data_movies_directors = await self.redis.get(key_movies_directors)
        if data_movies_directors:
            count_movies_director, movies_director = pickle.loads(data_movies_directors)
        else:
            count_movies_director, movies_director = await self._get_movies_directors(full_name)
            await self.redis.set(key_movies_directors, pickle.dumps([count_movies_director, movies_director]),
                                 expire=PERSON_CACHE_EXPIRE_IN_SECONDS)
        return count_movies_director, movies_director

    async def get_by_id(self, person_id: str):
        person, count_movies_actor, movies_actor = await self._get_actors_from_cache_or_elastic(person_id)
        count_movies_writers, movies_writer = await self._get_writers_from_cache_or_elastic(person_id)
        full_name = person['_source']['full_name']
        count_movies_director, movies_director = await self._get_directors_from_cache_or_elastic(person_id, full_name)
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
