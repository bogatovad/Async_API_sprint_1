import pytest
from elasticsearch import AsyncElasticsearch
from .settings import test_settings
import json
import uuid
import datetime
import requests
import aioredis

from .src.indexes import index_to_schema


@pytest.fixture
async def es_client():
    client = AsyncElasticsearch(hosts='http://elasticsearch:9200')
    yield client
    await client.close()
    requests.delete('http://elasticsearch:9200/movies')
    requests.delete('http://elasticsearch:9200/persons')


@pytest.fixture
async def redis_client():
    redis = await aioredis.create_redis_pool(('redis', '6379'), minsize=10, maxsize=20)
    yield redis
    # await redis.close()


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
        bulk_query = get_es_bulk_query(data, es_index, test_settings.es_id_field)
        response = await es_client.bulk(bulk_query, refresh=True)
        await es_client.close()
        if response['errors']:
            raise Exception(f'Ошибка записи данных в Elasticsearch')
    return inner


@pytest.fixture
def generate_es_data_person():
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
