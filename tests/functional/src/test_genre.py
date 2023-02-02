from http import HTTPStatus
import aiohttp
import pytest
from pytest_lazyfixture import lazy_fixture

from ..conftest import create_index
from ..settings import test_settings


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


@pytest.mark.parametrize(
    'expected_answer, es_data',
    [
        (
            10,
            lazy_fixture('generate_es_data_genre')
        ),
    ]
)
@pytest.mark.asyncio
async def test_get_all_genres(es_client, es_write_data, make_get_request, expected_answer, es_data):
    """Проверка вывода всех жанров."""
    await create_index(es_client)
    await es_write_data(es_data, 'genres')
    response = await make_get_request('genres')
    assert len(response.body) == expected_answer
    assert response.status == HTTPStatus.OK, f'{response.status} должен быть 200'


@pytest.mark.parametrize(
    'expected_answer, es_data',
    [
        (
            10,
            lazy_fixture('generate_es_data_genre')
        ),
    ]
)
@pytest.mark.asyncio
async def test_genre_cache(
        es_client, redis_client, es_write_data,
        make_get_request, expected_answer, es_data
    ):
    """Проверка работы кэша."""
    await create_index(es_client)
    await es_write_data(es_data, 'genres')
    await redis_client.flushall(async_op=True)
    keys = await redis_client.keys(pattern='*')

    assert len(keys) == 0

    response = await make_get_request('genres')
    keys = await redis_client.keys(pattern='*')

    assert len(keys) == 1
    assert expected_answer == len(response.body)
    assert response.status == HTTPStatus.OK, f'{response.status} должен быть 200'
