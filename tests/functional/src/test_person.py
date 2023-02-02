import aiohttp
import pytest
from pytest_lazyfixture import lazy_fixture

from ..conftest import create_index
from ..settings import test_settings


@pytest.mark.parametrize(
    'uuid_person, expected_answer, es_data',
    [
        (
            '42b40c6b-4d07-442f-b652-4ec1ee8b57gg',
            {'uuid': '42b40c6b-4d07-442f-b652-4ec1ee8b57gg', 'name': 'Ivan Petrov', 'role': [], 'film_ids': []},
            lazy_fixture('generate_es_data_person')
        ),
    ]
)
@pytest.mark.asyncio
async def test_get_person(es_client, es_write_data, uuid_person, expected_answer, es_data):
    """Проверка поиска персонажа по uuid."""
    await create_index(es_client)
    await es_write_data(es_data, 'persons')
    session = aiohttp.ClientSession()
    url = test_settings.SERVICE_URL + f'persons/{uuid_person}'

    async with session.get(url) as response:
        body = await response.json()

    assert body == expected_answer

