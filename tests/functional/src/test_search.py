import aiohttp
import pytest

from .indexes import index_to_schema
from ..conftest import generate_es_data, generate_es_data_person
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
async def test_search_movies(es_client, es_write_data, query_data, expected_answer):
    es_data = generate_es_data()
    await es_write_data(es_data, 'movies')
    session = aiohttp.ClientSession()
    url = test_settings.es_host + 'movies/_search'

    async with session.get(url) as response:
        status = response.status
        body = await response.json()

    await session.close()
    assert expected_answer == {'status': status, 'length': body['hits']['total']['value']}


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            {'search': 'The Star'},
            {'status': 200, 'length': 5}
        ),
    ]
)
@pytest.mark.asyncio
async def test_search_movies_paginator(es_client, es_write_data, query_data, expected_answer):
    es_data = generate_es_data()
    await es_write_data(es_data, 'movies')
    session = aiohttp.ClientSession()
    url = test_settings.service_url + 'films?page[number]=1&page[size]=5'
    async with session.get(url) as response:
        status = response.status
        body = await response.json()
    await session.close()
    assert expected_answer == {'status': status, 'length': len(body)}


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            {'search': 'The Star'},
            {'status': 200, 'length': 10}
        ),
        (
            {'search': 'New World'},
            {'status': 200, 'length': 10}
        ),
    ]
)
@pytest.mark.asyncio
async def test_search_movies_filtering(es_client, es_write_data, query_data, expected_answer):
    es_data = generate_es_data()
    await es_write_data(es_data, 'movies')
    session = aiohttp.ClientSession()
    url = test_settings.service_url + 'films?filter[genre]=Sci-Fi'
    async with session.get(url) as response:
        status = response.status
        body = await response.json()
    await session.close()
    assert expected_answer == {'status': status, 'length': len(body)}


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
async def test_search_movies_elastic(es_client, es_write_data, query_data, expected_answer):
    es_data = generate_es_data()
    await es_write_data(es_data, 'movies')
    session = aiohttp.ClientSession()
    url = test_settings.es_host + 'movies/_search'

    async with session.get(url) as response:
        status = response.status
        body = await response.json()

    await session.close()
    assert expected_answer == {'status': status, 'length': body['hits']['total']['value']}


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            {'search': 'Petr Ivanov'},
            {'status': 200, 'length': 60}
        ),
    ]
)
@pytest.mark.asyncio
async def test_search_persons_elastic(es_client, es_write_data, query_data, expected_answer):
    es_data = generate_es_data_person()
    await es_write_data(es_data, 'persons')
    session = aiohttp.ClientSession()
    url = test_settings.es_host + 'persons/_search'

    async with session.get(url) as response:
        status = response.status
        body = await response.json()

    await session.close()
    assert expected_answer == {'status': status, 'length': body['hits']['total']['value']}


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            {'search': 'The Star'},
            {'status': 200, 'length': 5}
        ),
    ]
)
@pytest.mark.asyncio
async def test_search_persons(es_client, es_write_data, query_data, expected_answer):
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
    url = test_settings.service_url + 'persons/search?query=Petr Ivanov&page[size]=5&page[index]=1'

    async with session.get(url) as response:
        status = response.status
        body = await response.json()

    assert expected_answer == {'status': status, 'length': len(body)}


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            {'search': 'The Star'},
            {'status': 200, 'length': 5}
        ),
    ]
)
@pytest.mark.asyncio
async def test_search_persons_cache(es_client, redis_client, es_write_data, query_data, expected_answer):
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

    # Очистим кэш перед запросом.
    keys = await redis_client.keys(pattern='*')
    for key in keys:
        await redis_client.delete(key)
    keys = await redis_client.keys(pattern='*')

    # Проверим что кэш пустой.
    assert len(keys) == 0

    # Делаем первый раз запрос.
    url = test_settings.service_url + 'persons/search?query=Petr Ivanov&page[size]=5&page[index]=1'

    async with session.get(url) as response:
        status = response.status
        body = await response.json()

    keys = await redis_client.keys(pattern='*')

    # Проверяем кэш.
    assert len(keys) == 16
    assert expected_answer == {'status': status, 'length': len(body)}





