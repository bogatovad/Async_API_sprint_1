import http

import aiohttp
import pytest
from pytest_lazyfixture import lazy_fixture

from ..conftest import create_index
from ..settings import test_settings


@pytest.mark.parametrize(
    'uuid_film, expected_answer, es_data',
    [
        (
            '12bb1b7e-b039-4f66-9248-b35d795e38f6',
            {
                'uuid': str('12bb1b7e-b039-4f66-9248-b35d795e38f6'),
                'imdb_rating': 8.5,
                'genre': ['Action', 'Sci-Fi'],
                'title': 'The Star',
                'description': 'New World',
                'directors': ['Stan'],
                'actors': [
                    {'id': '111', 'name': 'Ann'},
                    {'id': '222', 'name': 'Bob'},

                ],
                'writers': [
                    {'id': '333', 'name': 'Ben'},
                    {'id': '444', 'name': 'Howard'}
                ],
            },
            lazy_fixture('generate_es_data')
        ),
    ]
)
@pytest.mark.asyncio
async def test_get_film(es_client, es_write_data, uuid_film, expected_answer, es_data):

    await create_index(es_client)
    await es_write_data(es_data, 'movies')

    url = test_settings.service_url + f'films/{uuid_film}'

    session = aiohttp.ClientSession()
    async with session.get(url) as response:
        body = await response.json()

    assert uuid_film == body['uuid']
    assert body == expected_answer


@pytest.mark.asyncio
async def test_nonexistent_film(es_client):

    url = test_settings.service_url + 'films/nonexistentfilm'

    session = aiohttp.ClientSession()
    async with session.get(url) as response:
        code = response.status

    assert code == http.HTTPStatus.NOT_FOUND


@pytest.mark.parametrize(
    'expected_answer', ({'status': http.HTTPStatus.OK, 'length': 61},)
)
@pytest.mark.asyncio
async def test_all_films(es_client, es_write_data, generate_es_data, expected_answer,
                         generate_expected_answer_for_all_films):
    await create_index(es_client)
    await es_write_data(generate_es_data, 'movies')

    url = test_settings.service_url + 'films/?page[size]=61&page[number]=1'

    session = aiohttp.ClientSession()
    async with session.get(url) as response:
        code = response.status
        body = await response.json()

    assert code == expected_answer['status']
    assert len(body) == expected_answer['length']
    for response_item, expected_item in zip(body, generate_expected_answer_for_all_films):
        assert (
            response_item['uuid'], response_item['title'], response_item['imdb_rating'] ==
            expected_item
        )


@pytest.mark.parametrize(
    'expected_answer',  ({'status': http.HTTPStatus.OK, 'length': 1},)
)
@pytest.mark.asyncio
async def test_caching_all_films(es_client, redis_client, es_write_data, generate_es_data, expected_answer):
    await create_index(es_client)
    await es_write_data(generate_es_data, 'movies')

    # Очистим кэш перед запросом.
    keys = await redis_client.keys(pattern='*')
    for key in keys:
        await redis_client.delete(key)

    keys = await redis_client.keys(pattern='*')
    # Проверим что кэш пустой.
    assert len(keys) == 0

    # Делаем первый раз запрос.
    url = test_settings.service_url + 'films/?page[size]=61&page[number]=1'

    session = aiohttp.ClientSession()
    async with session.get(url) as response:
        code = response.status

    keys = await redis_client.keys('*')

    assert code == expected_answer['status']
    assert len(keys) == expected_answer['length']
