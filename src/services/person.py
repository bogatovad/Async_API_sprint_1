import pickle
from functools import lru_cache

from aioredis import Redis
from elasticsearch import AsyncElasticsearch

from db.elastic import get_elastic
from db.redis import get_redis
from fastapi import Depends
from models.api.film import Film
from models.api.person import PersonFull
from services.paginator import Paginator

PERSON_CACHE_EXPIRE_IN_SECONDS = 60 * 5


class PersonService(Paginator):
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def search_persons(self, query: str, page: int, size: int):
        body = {
            "query": {
                "match": {
                    "full_name": f"{query}"
                }
            },
            "sort": {"id": "asc"},
            "size": f"{size}",
        }
        body_copy = body.copy()
        body_copy["index"] = "person"
        key_person_search = pickle.dumps(body_copy)
        persons = await self.redis.get(key_person_search)

        if persons:
            loads_persons = pickle.loads(persons)
        else:
            loads_persons = await self.paginator("persons", body, page)
            await self.redis.set(key_person_search, pickle.dumps(loads_persons), expire=PERSON_CACHE_EXPIRE_IN_SECONDS)
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
        return [Film(**movie['_source']) for movie in docs_actors['hits']['hits']]

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
        return PersonFull(**person['_source'], role=role, film_ids=film_ids)


@lru_cache()
def get_person_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(redis, elastic)
