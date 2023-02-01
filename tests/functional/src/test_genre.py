import aiohttp
import pytest

from .indexes import index_to_schema
from ..conftest import generate_es_data, generate_es_data_person, make_get_request
from ..settings import test_settings


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            {'uuid': '1111-2222-3333-4444'},
            404
        ),
    ]
)
@pytest.mark.asyncio
async def test_nonexisting_genre(make_get_request, query_data, expected_answer):
    response = await make_get_request(f'genres/{query_data}')
    assert expected_answer == response.status


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            {'uuid': '72a78147-b2c7-4188-9310-5139c32b2c11'},
            {'uuid': '42b40c6b-4d07-442f-b652-4ec1ee8b57dd', 'name': 'Petr Ivanov', 'role': [], 'film_ids': []}
        ),
    ]
)
@pytest.mark.asyncio
async def test_get_genre_by_id(es_client, es_write_data, query_data, expected_answer):
    for index in ("movies", "genres", "persons"):
        data_create_index = {
            "index": "genre",
            "ignore": 400,
            "body": index_to_schema.get(index)
        }
        await es_client.indices.create(
           **data_create_index
        )

    es_data = generate_es_data_person()
    await es_write_data(es_data, 'persons')
    session = aiohttp.ClientSession()

    url_es = test_settings.ES_HOST + 'persons/_search'

    async with session.get(url_es) as response:
        body = await response.json()
        uuid_person = body['hits']['hits'][0]['_id']

    url = test_settings.SERVICE_URL + f'persons/{uuid_person}'

    async with session.get(url) as response:
        body = await response.json()

    assert body['uuid'] == uuid_person
