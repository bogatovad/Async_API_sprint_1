from http.client import HTTPResponse
import aiohttp
import pytest
from elasticsearch import AsyncElasticsearch
from .settings import test_settings
from pydantic import BaseModel
from .utils.elastic_manager import ElasticManager


@pytest.fixture
async def es_client():
    client = AsyncElasticsearch(
        hosts=f'{test_settings.ELASTIC_HOST}:{test_settings.ELASTIC_PORT}', validate_cert=False, use_ssl=False
    )
    test_data_manager = ElasticManager(elastic_client=client)
    await test_data_manager.create_test_data()
    yield client
    await test_data_manager.delete_elastic_test_data()
    await client.close()


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
