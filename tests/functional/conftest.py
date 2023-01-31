import json
from http.client import HTTPResponse
import aiohttp
import pytest
from elasticsearch import AsyncElasticsearch
from .settings import test_settings
from pydantic import BaseModel
from .utils.elastic_manager import ElasticManager
import uuid
import datetime
import requests


@pytest.fixture
async def es_client():
    client = AsyncElasticsearch(hosts=test_settings.ELASTIC_HOST, validate_cert=False, use_ssl=False)
    test_data_manager = ElasticManager(elastic_client=client)
    await test_data_manager.create_test_data()
    yield client
    await test_data_manager.delete_elastic_test_data()
    await client.close()
    requests.delete('http://elasticsearch:9200/movies')
    requests.delete('http://elasticsearch:9200/persons')


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
        await es_client.close()
        if response['errors']:
            raise Exception(f'Ошибка записи данных в Elasticsearch')


@pytest.fixture
async def session(es_client):
    session = aiohttp.ClientSession()
    yield session
    await session.close()


class HTTPResponse(BaseModel):
    body: dict
    status: int


@pytest.fixture
def make_get_request(session):
    async def inner(endpoint: str, params: dict = None) -> HTTPResponse:
        params = params or {}
        url = f"{test_settings.SERVICE_URL}/api/v1/{endpoint}"
        async with session.get(url, params=params) as response:
            return HTTPResponse(
                body=response.json(),
                status=response.status,
            )
    return inner


def generate_es_data_person():
    return [
        {
            'id': str(uuid.uuid4()),
            'full_name': 'Petr Ivanov',
        }
        for _ in range(60)
    ]


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
                # {'id': '44', 'name': 'Petr Ivanov'}

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
