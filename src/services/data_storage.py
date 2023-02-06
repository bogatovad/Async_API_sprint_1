import backoff
from abc import ABC, abstractmethod

from elasticsearch import NotFoundError, ConnectionError

from models.film import Film, FilmShort
from models.genre import Genre
from services.utils import es_search_template


class DataStorage(ABC):
    """Интерфейс, реализующий доступ к базе."""

    @abstractmethod
    async def get_by_id(self, *args, **kwargs):
        pass

    @abstractmethod
    async def search(self):
        pass

    @abstractmethod
    async def get_list(self):
        pass

    @abstractmethod
    async def get_alike(self):
        pass

    @abstractmethod
    async def get_persons_film_by_id(self):
        pass


class AsyncElasticDataStorage(DataStorage):
    """Класс, реализующий доступ к эластику."""

    def __init__(self, es):
        self.elastic = es

    @backoff.on_exception(backoff.expo, ConnectionError, max_time=10, factor=2)
    async def paginator(self, index: str, query_params: dict, page: int):
        doc = await self.elastic.search(
            index=index,
            body=query_params
        )

        data = doc['hits']['hits']

        if not data:
            return []

        last_item = data[-1]
        search_after = last_item['sort']
        query_params['search_after'] = search_after

        for item_page in range(1, int(page)):
            docs = await self.elastic.search(index=index, body=query_params)
            data = docs['hits']['hits']
            if not data:
                break
            last_item = data[-1]
            search_after = last_item['sort']
            query_params['search_after'] = search_after

        return data

    @backoff.on_exception(backoff.expo, ConnectionError, max_time=10, factor=2)
    async def _get_data_by_id_movies(self, *args, **kwargs):
        """Поиск по id по фильмам."""
        params, = args
        index = params.get('index')
        try:
            film_id: str = params.get('film_id')
            doc = await self.elastic.get(index, film_id)
        except NotFoundError:
            return None
        return Film(**doc['_source'])

    @backoff.on_exception(backoff.expo, ConnectionError, max_time=10, factor=2)
    async def _get_actors(self, *args, **kwargs):
        params, = args
        person_id: str = params.get('person_id')
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

    @backoff.on_exception(backoff.expo, ConnectionError, max_time=10, factor=2)
    async def _get_writers(self, *args, **kwargs):
        params, = args
        person_id: str = params.get('person_id')
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

    async def _get_directors(self, full_name: str):
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

    @backoff.on_exception(backoff.expo, ConnectionError, max_time=10, factor=2)
    async def _get_data_by_id_persons(self, *args, **kwargs):
        """Поиск по id по персонажам."""
        person, count_movies_actor, movies_actor = await self._get_actors(*args)
        count_movies_writers, movies_writer = await self._get_writers(*args)
        full_name = person['_source']['full_name']
        count_movies_director, movies_director = await self._get_directors(full_name)
        film_ids = list(set(movies_actor + movies_writer + movies_director))
        role = [
            role[0] for role in (
                ('actor', count_movies_actor),
                ('writer', count_movies_writers),
                ('director', count_movies_director)
            ) if role[1] != 0
        ]
        return dict(
            **person['_source'],
            role=role,
            film_ids=film_ids
        )

    @backoff.on_exception(backoff.expo, ConnectionError, max_time=10, factor=2)
    async def _get_data_by_id_genres(self, *args, **kwargs):
        params, = args
        genre_id: str = params.get("genre_id")
        try:
            doc = await self.elastic.get('genres', genre_id)
        except NotFoundError:
            return None
        doc = doc['_source']
        return Genre(**doc)

    @backoff.on_exception(backoff.expo, ConnectionError, max_time=10, factor=2)
    async def get_by_id(self, *args, **kwargs):
        params, = args
        index = params.get('index')
        index_to_method: dict = {
            'movies': self._get_data_by_id_movies,
            'persons': self._get_data_by_id_persons,
            'genres': self._get_data_by_id_genres,
        }
        return await index_to_method[index](*args, **kwargs)

    @backoff.on_exception(backoff.expo, ConnectionError, max_time=10, factor=2)
    async def _search_persons(self, *args, **kwargs):
        """Реализация поиска для персонажей."""
        params, = args
        index = params.get('index')
        page, body = es_search_template(index, *args)
        loads_persons = await self.paginator(index, body, page)
        return [
            await self.get_by_id(
                dict(
                    person_id=person['_source']['id'],
                    request=params.get('request'),
                    index='persons'
                )
            )
            for person in loads_persons
        ]

    @backoff.on_exception(backoff.expo, ConnectionError, max_time=10, factor=2)
    async def _search_movies(self, *args, **kwargs):
        """Реализация поиска для фильмов."""
        params, = args
        index = params.get('index')
        page, body = es_search_template(index, *args)
        loads_movies = await self.paginator(index, body, page)
        return [Film(**movie['_source']) for movie in loads_movies]

    @backoff.on_exception(backoff.expo, ConnectionError, max_time=10, factor=2)
    async def search(self, *args, **kwargs):
        params, = args
        index = params.get('index')
        index_to_method: dict = {
            'movies': self._search_movies,
            'persons': self._search_persons,
        }
        return await index_to_method[index](*args, **kwargs)

    @backoff.on_exception(backoff.expo, ConnectionError, max_time=10, factor=2)
    async def _get_list_genres(self, *args, **kwargs):
        try:
            docs = await self.elastic.search(index="genres", body={"query": {"match_all": {}}})
        except NotFoundError:
            return []
        return [Genre(**genre['_source']) for genre in docs['hits']['hits']]

    @backoff.on_exception(backoff.expo, ConnectionError, max_time=10, factor=2)
    async def _get_list_movies(self, *args, **kwargs):
        params, = args
        index = params.get('index')
        page, body = es_search_template(index, *args)
        loads_films = await self.paginator(index, body, page)
        return [Film(**film['_source']) for film in loads_films]

    @backoff.on_exception(backoff.expo, ConnectionError, max_time=10, factor=2)
    async def get_list(self, *args, **kwargs):
        """Метод реализует получение списка объектов."""
        params, = args
        index = params.get('index')
        index_to_method: dict = {
            'movies': self._get_list_movies,
            'genres': self._get_list_genres,
        }
        return await index_to_method[index](*args, **kwargs)

    @backoff.on_exception(backoff.expo, ConnectionError, max_time=10, factor=2)
    async def get_alike(self, *args, **kwargs):
        params, = args
        film = await self.get_by_id(dict(
            film_id=params.get('film_id'),
            request=params.get('request'),
            index='movies'
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

    @backoff.on_exception(backoff.expo, ConnectionError, max_time=10, factor=2)
    async def get_persons_film_by_id(self, *args, **kwargs):
        params, = args
        person_id: str = params.get('person_id')
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
