import aiohttp
import pytest

from ..conftest import generate_es_data, generate_es_data_person
from ..settings import test_settings
from .indexes import index_to_schema


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
    url = test_settings.ES_HOST + '/movies/_search'

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
    url = test_settings.SERVICE_URL + 'films?page[number]=1&page[size]=5'
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
    url = test_settings.SERVICE_URL + 'films?filter[genre]=Sci-Fi'
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
async def test_search_movies(es_client, es_write_data, query_data, expected_answer):
    es_data = generate_es_data()
    await es_write_data(es_data, 'movies')
    session = aiohttp.ClientSession()
    url = test_settings.ES_HOST + 'movies/_search'

    async with session.get(url) as response:
        status = response.status
        body = await response.json()
        print(f'bod123y {body}')

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
async def test_search_persons(es_client, es_write_data, query_data, expected_answer):
    es_data = generate_es_data_person()
    await es_write_data(es_data, 'persons')
    session = aiohttp.ClientSession()
    url = test_settings.ES_HOST + 'persons/_search'

    async with session.get(url) as response:
        status = response.status
        body = await response.json()

    await session.close()
    assert expected_answer == {'status': status, 'length': body['hits']['total']['value']}




