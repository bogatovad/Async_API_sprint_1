import http

import aiohttp
import pytest

from ..conftest import generate_single_film
from ..settings import test_settings
from .indexes import index_to_schema

data_create_index = {
    "index": 'movies',
    "ignore": 400,
    "body": index_to_schema.get('movies')
}


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            {'uuid': '12bb1b7e-b039-4f66-9248-b35d795e38f6'},
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
async def test_get_film(es_client, es_write_data, query_data, expected_answer):

    await es_client.indices.create(
        **data_create_index
    )
    es_data = generate_single_film()

    await es_write_data(es_data, 'movies')
    session = aiohttp.ClientSession()

    url_es = test_settings.ES_HOST + 'movies/_search'

    async with session.get(url_es) as response:
        body = await response.json()
        data = body['hits']['hits'][0]['_source']
        uuid_film = data['id']

    url = test_settings.SERVICE_URL + f'films/{uuid_film}'

    async with session.get(url) as response:
        body = await response.json()

    assert uuid_film == body['uuid']
    assert body == expected_answer


@pytest.mark.asyncio
async def test_nonexistent_film(es_client):

    url = test_settings.SERVICE_URL + f'films/nonexistentfilm'

    session = aiohttp.ClientSession()
    async with session.get(url) as response:
        code = response.status

    assert code == http.HTTPStatus.NOT_FOUND
