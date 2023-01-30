import aiohttp
import pytest

from ..conftest import generate_es_data_person
from ..settings import test_settings


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            {'search': 'The Star'},
            {'status': 200, 'length': 60}
        ),
    ]
)
@pytest.mark.asyncio
async def test_person(es_client, es_write_data, query_data, expected_answer):
    es_data = generate_es_data_person()
    await es_write_data(es_data, 'persons')
    session = aiohttp.ClientSession()
    url = test_settings.es_host + '/persons/_search'

    async with session.get(url) as response:
        status = response.status
        body = await response.json()

    await session.close()
    assert expected_answer == {'status': status, 'length': body['hits']['total']['value']}