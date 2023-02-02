import http

import aiohttp
import pytest

from ..conftest import generate_single_film
from ..settings import test_settings
from ..utils.indexes import index_to_schema
from ..conftest import create_index

data_create_index = {
    "index": 'movies',
    "ignore": 400,
    "body": index_to_schema.get('movies')
}


@pytest.mark.parametrize(
    'uuid_film, expected_answer',
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
            }
        ),
    ]
)
@pytest.mark.asyncio
async def test_get_film(es_client, es_write_data, uuid_film, expected_answer):

    await create_index(es_client)
    es_data = generate_single_film()

    await es_write_data(es_data, 'movies')

    url = test_settings.SERVICE_URL + f'films/{uuid_film}'

    session = aiohttp.ClientSession()
    async with session.get(url) as response:
        body = await response.json()

    assert uuid_film == body['uuid']
    assert body == expected_answer


@pytest.mark.asyncio
async def test_nonexistent_film(es_client):

    url = test_settings.SERVICE_URL + 'films/nonexistentfilm'

    session = aiohttp.ClientSession()
    async with session.get(url) as response:
        code = response.status

    assert code == http.HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_all_films(es_client, es_write_data, generate_es_data):
    await create_index(es_client)
    await es_write_data(generate_es_data, 'movies')

    url = test_settings.SERVICE_URL + 'films/?page[size]=60&page[number]=1'

    session = aiohttp.ClientSession()
    async with session.get(url) as response:
        code = response.status
        body = await response.json()

    assert code == http.HTTPStatus.OK
    assert len(body) == 60
    for response_item, expected_item in zip(body, generate_es_data):
        assert (
            response_item['uuid'], response_item['title'], response_item['imdb_rating'] ==
            expected_item['id'], expected_item['title'], expected_item['imdb_rating']
        )
