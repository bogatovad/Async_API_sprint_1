import aiohttp
import pytest
from elasticsearch import AsyncElasticsearch
import json
import uuid
import datetime
import requests

from .settings import test_settings
from .src.indexes import index_to_schema
from .utils.models import HTTPResponse


@pytest.fixture(scope='function')
async def es_client():
    client = AsyncElasticsearch(hosts='http://elasticsearch:9200')
    yield client
    await client.close()
    requests.delete('http://elasticsearch:9200/movies')
    requests.delete('http://elasticsearch:9200/persons')


@pytest.fixture(scope='function')
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


def get_es_bulk_query(es_data, es_index, es_id_field):
    bulk_query = []
    for row in es_data:
        bulk_query.extend([
            json.dumps({'index': {'_index': es_index, '_id': row[es_id_field]}}),
            json.dumps(row)
        ])
    return '\n'.join(bulk_query) + '\n'


@pytest.fixture
def es_write_data(es_client):
    async def inner(data: list[dict], es_index: str):
        bulk_query = get_es_bulk_query(data, es_index, test_settings.ES_ID_FIELD)
        response = await es_client.bulk(bulk_query, refresh=True)
        if response['errors']:
            raise Exception(f'Ошибка записи данных в Elasticsearch')
    return inner


@pytest.fixture
def make_get_request(session):
    async def inner(endpoint: str, params: dict = {}) -> HTTPResponse:
        url = f"{test_settings.SERVICE_URL}{endpoint}"
        print(url)
        async with session.get(url, params=params) as response:
            return HTTPResponse(
                body=await response.json(),
                status=response.status,
            )

    return inner


@pytest.fixture
def generate_es_data_person():
    """Фикстура для генерации данных по персонажам."""
    persons = [
        {
            'id': str(uuid.uuid4()),
            'full_name': 'Petr Ivanov',
        }
        for _ in range(60)
    ]
    persons.extend([
        {'id': '42b40c6b-4d07-442f-b652-4ec1ee8b57gg', 'full_name': 'Ivan Petrov'}
    ])
    return persons


@pytest.fixture
def generate_es_data():
    """Фикстура для генерации данных по фильмам."""
    return [
        {
            'id': str(uuid.uuid4()),
            'imdb_rating': 8.5,
            'genre': ['Action', 'Sci-Fi'],
            'title': 'The Star',
            'description': 'New World',
            'director': ['Stan'],
            'actors_names': ['Ann', 'Bob'],
            'writers_names': ['Ben', 'Howard'],
            'actors': [
                {'id': '111', 'name': 'Ann'},
                {'id': '222', 'name': 'Bob'},
            ],
            'writers': [
                {'id': '333', 'name': 'Ben'},
                {'id': '444', 'name': 'Howard'}
            ],
            'created_at': datetime.datetime.now().isoformat(),
            'updated_at': datetime.datetime.now().isoformat(),
            'film_work_type': 'movie'
        }
        for _ in range(60)
    ]

@pytest.fixture
def generate_es_data_genre():
    """Фикстура для генерации данных по жанрам."""
    genres = [
            {
                'id': str(uuid.uuid4()),
                'name': 'Thriller',
                'description': 'Thrilling and scary'
            }
            for _ in range(9)
        ]
    genres.append(
        {
            'id': '9c91a5b2-eb70-4889-8581-ebe427370edd',
            'name': 'Musical',
            'description': 'Nice and dancy'
        }
    )
    return genres

async def create_index(es_client):
    """Метод создает индексы для тестирования."""
    for index in ("movies", "genres", "persons"):
        data_create_index = {
            "index": index,
            "ignore": 400,
            "body": index_to_schema.get(index)
        }
        await es_client.indices.create(
            **data_create_index
        )

