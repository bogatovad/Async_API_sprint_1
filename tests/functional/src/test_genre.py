from http import HTTPStatus

import pytest
from pytest_lazyfixture import lazy_fixture

from ..conftest import create_index


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            {'uuid': '1111-2222-3333-4444'},
            HTTPStatus.NOT_FOUND
        ),
    ]
)
@pytest.mark.asyncio
async def test_non_existing_genre(make_get_request, query_data, expected_answer):
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
    assert response.status == HTTPStatus.OK, f'{response.status} должен быть 200'
