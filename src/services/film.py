from functools import lru_cache
from typing import Optional

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError

from db.elastic import get_elastic
from db.redis import get_redis
from fastapi import Depends
from models.api.person import PersonFull
from models.services.film import Film
from models.services.genre import GenreId
from .base_service import BaseService
from .utils import es_search_template

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5


class FilmService(BaseService):

    async def get_all_films(self):
        body = {
            'query': {'match_all': {}},
            'sort': {"imdb_rating": "desc"}
        }

        doc = await self.elastic.search(
            index=self.index,
            body=body
        )
        return doc

    async def get_search(self, query_params):
        if query_params:
            body = es_search_template(query_params)
        else:
            body = await self.get_all_films()

        doc = await self.elastic.search(index=self.index, body=body)

        return doc


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


class PersonService:
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

        docs = await self.elastic.search(index="persons", body=body)
        data = docs['hits']['hits']

        if not data:
            return []

        last_item = data[-1]
        search_after = last_item['sort']
        body['search_after'] = search_after

        for item_page in range(1, page):
            docs = await self.elastic.search(index="persons", body=body)
            data = docs['hits']['hits']
            if not data:
                break
            last_item = data[-1]
            search_after = last_item['sort']
            body['search_after'] = search_after

        return [await self.get_by_id(person['_source']['id']) for person in data]

    async def get_film_by_id(self, person_id: str):
        docs_actors = await self.elastic.search(index="movies", body=
        {
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
        })
        return [Film(**movie['_source']) for movie in docs_actors['hits']['hits']]

    async def get_by_id(self, person_id: str):
        person = await self.elastic.get("persons", person_id)
        docs_actors = await self.elastic.search(index="movies", body=
        {
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
        })
        count_movies_actor = docs_actors['hits']['total']['value']
        movies_actor = [movie['_source']['id'] for movie in docs_actors['hits']['hits']]

        docs_writes = await self.elastic.search(index="movies", body=
        {
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
        })

        count_movies_writers = docs_writes['hits']['total']['value']
        movies_writer = [movie['_source']['id'] for movie in docs_writes['hits']['hits']]
        full_name = person['_source']['full_name']
        docs_director = await self.elastic.search(index="movies", body=
        {
            "query": {
                "match": {
                    "director": f"{full_name}"
                }
            }
        })

        count_movies_director = docs_director['hits']['total']['value']
        movies_director = [movie['_source']['id'] for movie in docs_director['hits']['hits']]
        film_ids = list(set(movies_actor + movies_writer + movies_director))
        role = [
            role[0] for role in
                (('actor', count_movies_actor), ('writer', count_movies_writers), ('director', count_movies_director))
                if role[1] != 0
        ]
        return PersonFull(**person['_source'], role=role, film_ids=film_ids)


@lru_cache()
def get_film_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic, 'movies', Film)

@lru_cache()
def get_genre_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis, elastic)


@lru_cache()
def get_person_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(redis, elastic)