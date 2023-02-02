from http import HTTPStatus

import aiohttp
import pytest
from pytest_lazyfixture import lazy_fixture

from ..conftest import create_index
from ..settings import test_settings

@pytest.mark.parametrize(
    'expected_answer, es_data',
    [
        (
            {'status': HTTPStatus.OK, 'length': 60},
            lazy_fixture('generate_es_data')
        ),
    ]
)
@pytest.mark.asyncio
async def test_load_movies_elastic(es_write_data,  expected_answer, es_data):
    """Проверка загрузки данных movies в elasticsearch."""
    await es_write_data(es_data, 'movies')
    session = aiohttp.ClientSession()
    url = test_settings.ES_HOST + 'movies/_search'

    async with session.get(url) as response:
        status = response.status
        body = await response.json()

    await session.close()
    assert expected_answer == {'status': status,
                               'length': body['hits']['total']['value']}


@pytest.mark.parametrize(
    'expected_answer, es_data',
    [
        (
            {'status': HTTPStatus.OK, 'length': 5},
            lazy_fixture('generate_es_data')
        ),
    ]
)
@pytest.mark.asyncio
async def test_search_movies_paginator(es_write_data, expected_answer, es_data):
    """Проверка пагинации при выдаче фильмов."""
    await es_write_data(es_data, 'movies')
    session = aiohttp.ClientSession()
    url = test_settings.SERVICE_URL + 'films?page[number]=1&page[size]=5'
    async with session.get(url) as response:
        status = response.status
        body = await response.json()

    await session.close()
    assert expected_answer == {'status': status, 'length': len(body)}


@pytest.mark.parametrize(
    'expected_answer, es_data',
    [
        (
            {'status': HTTPStatus.OK, 'length': 10},
            lazy_fixture('generate_es_data')
        ),
        (
            {'status': HTTPStatus.OK, 'length': 10},
            lazy_fixture('generate_es_data')
        ),
    ]
)
@pytest.mark.asyncio
async def test_search_movies_filtering(es_write_data, expected_answer, es_data):
    """Проверка фильтрации в выдаче фильмов."""
    await es_write_data(es_data, 'movies')
    session = aiohttp.ClientSession()
    url = test_settings.SERVICE_URL + 'films?filter[genre]=Sci-Fi'
    async with session.get(url) as response:
        status = response.status
        body = await response.json()

    await session.close()
    assert expected_answer == {'status': status, 'length': len(body)}


@pytest.mark.parametrize(
    'expected_answer, es_data',
    [
        (
            {'status': HTTPStatus.OK, 'length': 61},
            lazy_fixture('generate_es_data_person')
        ),
    ]
)
@pytest.mark.asyncio
async def test_load_persons_elastic(es_write_data, expected_answer, es_data):
    """Проверка загрузки данных persons в elasticsearch."""
    await es_write_data(es_data, 'persons')
    session = aiohttp.ClientSession()
    url = test_settings.ES_HOST + 'persons/_search'

    async with session.get(url) as response:
        status = response.status
        body = await response.json()

    await session.close()
    assert expected_answer == {'status': status,
                               'length': body['hits']['total']['value']}


@pytest.mark.parametrize(
    'expected_answer, es_data',
    [
        (
            {'status': HTTPStatus.OK, 'length': 5},
            lazy_fixture('generate_es_data_person')
        ),
    ]
)
@pytest.mark.asyncio
async def test_search_persons(es_client, es_write_data, expected_answer, es_data):
    """Проверка поиска по персонажам."""
    await create_index(es_client)
    await es_write_data(es_data, 'persons')
    session = aiohttp.ClientSession()
    url = test_settings.SERVICE_URL + \
        'persons/search?query=Petr Ivanov&page[size]=5&page[index]=1'

    async with session.get(url) as response:
        status = response.status
        body = await response.json()

    assert expected_answer == {'status': status, 'length': len(body)}


@pytest.mark.parametrize(
    'expected_answer, es_data',
    [
        (
            {'status': HTTPStatus.OK, 'length': 5},
            lazy_fixture('generate_es_data_person')
        ),
    ]
)
@pytest.mark.asyncio
async def test_search_persons_cache(es_client, redis_client, es_write_data, expected_answer, es_data):
    """Проверка работы кэша."""
    await create_index(es_client)
    await es_write_data(es_data, 'persons')
    session = aiohttp.ClientSession()

    # Очистим кэш перед запросом.
    keys = await redis_client.keys(pattern='*')
    for key in keys:
        await redis_client.delete(key)
    keys = await redis_client.keys(pattern='*')

    # Проверим что кэш пустой.
    assert len(keys) == 0

    # Делаем первый раз запрос.
    url = test_settings.SERVICE_URL + \
        'persons/search?query=Petr Ivanov&page[size]=5&page[index]=1'

    async with session.get(url) as response:
        status = response.status
        body = await response.json()

    keys = await redis_client.keys(pattern='*')

    # Проверяем кэш.
    assert len(keys) == 16
    assert expected_answer == {'status': status, 'length': len(body)}


@pytest.mark.parametrize(
    'expected_answer, es_data',
    [
        (
            {"detail": "person not found"},
            lazy_fixture('generate_es_data_person')
        ),
    ]
)
@pytest.mark.asyncio
async def test_search_persons_not_found(es_client, es_write_data, expected_answer, es_data):
    """Проверка поиска по персонажам. Персонаж не найден."""
    await create_index(es_client)
    await es_write_data(es_data, 'persons')
    session = aiohttp.ClientSession()
    url = test_settings.SERVICE_URL + 'persons/search?query=Petr123'

    async with session.get(url) as response:

        # not found.
        body = await response.json()

    assert expected_answer == body
