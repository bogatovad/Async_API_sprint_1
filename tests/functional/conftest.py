import json
import uuid

import aiohttp
import aioredis
import pytest
import requests
from core.config import settings
from elasticsearch import AsyncElasticsearch

from .settings import test_settings
from .utils.indexes import index_to_schema
from .utils.models import HTTPResponse

from glob import glob


def delete_data_from_elastic(url_elastic: str, urls: list[str]) -> None:
    for url in urls:
        requests.delete(f'{url_elastic}/{url}')


@pytest.fixture(scope='function')
async def es_client():
    url_elastic: str = f'http://{settings.ELASTIC_HOST}:{settings.ELASTIC_PORT}'
    client = AsyncElasticsearch(hosts=url_elastic)
    yield client
    await client.close()
    delete_data_from_elastic(url_elastic, ['movies', 'persons', 'genre'])


@pytest.fixture
async def redis_client():
    redis_host: str = settings.REDIS_HOST
    redis_port: str = settings.REDIS_PORT
    redis = await aioredis.create_redis_pool((redis_host, redis_port), minsize=10, maxsize=20)
    yield redis


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
        async with session.get(url, params=params) as response:
            return HTTPResponse(
                body=await response.json(),
                status=response.status,
            )
    return inner


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


def refactor(string: str) -> str:
    return string.replace("/", ".").replace("\\", ".").replace(".py", "")


pytest_plugins = [
    refactor(fixture) for fixture in glob("tests/fixtures/*.py") if "__" not in fixture
]