import aiohttp
import pytest

from .indexes import index_to_schema
from ..conftest import generate_es_data_person
from ..settings import test_settings


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            {'uuid': '42b40c6b-4d07-442f-b652-4ec1ee8b57dd'},
            {'uuid': '42b40c6b-4d07-442f-b652-4ec1ee8b57dd', 'name': 'Petr Ivanov', 'role': [], 'film_ids': []}
        ),
    ]
)
@pytest.mark.asyncio
async def test_get_person(es_client, es_write_data, query_data, expected_answer):
    for index in ("movies", "genres", "persons"):
        data_create_index = {
            "index": index,
            "ignore": 400,
            "body": index_to_schema.get(index)
        }
        await es_client.indices.create(
           **data_create_index
        )

    es_data = generate_es_data_person()
    await es_write_data(es_data, 'persons')
    session = aiohttp.ClientSession()

    url_es = test_settings.es_host + 'persons/_search'

    async with session.get(url_es) as response:
        body = await response.json()
        uuid_person = body['hits']['hits'][0]['_id']

    url = test_settings.service_url + f'persons/{uuid_person}'

    async with session.get(url) as response:
        body = await response.json()

    assert body['uuid'] == uuid_person