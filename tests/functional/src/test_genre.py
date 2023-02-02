import aiohttp
import pytest
from pytest_lazyfixture import lazy_fixture

from ..utils.indexes import index_to_schema
from ..conftest import (generate_es_data, generate_es_data_person,
                         generate_es_data_genre, make_get_request,
                         create_index)
from ..utils.models import Genre
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
    'uuid_genre, expected_answer, es_data',
    [
        (
            '9c91a5b2-eb70-4889-8581-ebe427370edd',
            {'uuid': '9c91a5b2-eb70-4889-8581-ebe427370edd', 'name': 'Musical'},
            lazy_fixture('generate_es_data_genre')
        ),
    ]
)
@pytest.mark.asyncio
async def test_get_genre_by_id(es_client, es_write_data, make_get_request, uuid_genre, expected_answer, es_data):
    """Проверка поиска жанра по uuid."""
    await create_index(es_client)
    await es_write_data(es_data, 'genres')
    response = await make_get_request(f'genres/{uuid_genre}')
    assert response.body == expected_answer
    assert response.status == 200, f'{response.status}должен быть 200'