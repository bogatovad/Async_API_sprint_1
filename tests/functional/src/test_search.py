import datetime
import uuid

import aiohttp
import pytest
from ..settings import test_settings


def generate_es_data():
    return [
        {
            'id': str(uuid.uuid4()),
            'imdb_rating': 8.5,
            'genre': ['Action', 'Sci-Fi'],
            'title': 'The Star',
            'description': 'New World',
            'director': ['Stan'],
            'actors_names': ['Ann', 'Bob'],
            'writers_names': ['Ben', 'Howard'],
            'actors': [
                {'id': '111', 'name': 'Ann'},
                {'id': '222', 'name': 'Bob'}
            ],
            'writers': [
                {'id': '333', 'name': 'Ben'},
                {'id': '444', 'name': 'Howard'}
            ],
            'created_at': datetime.datetime.now().isoformat(),
            'updated_at': datetime.datetime.now().isoformat(),
            'film_work_type': 'movie'
        }
        for _ in range(60)
    ]


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
@pytest.mark.asyncio
async def test_search(es_client, es_write_data, query_data, expected_answer):
    es_data = generate_es_data()
    await es_write_data(es_data)
    session = aiohttp.ClientSession()
    url = test_settings.es_host + '/movies/_search'

    async with session.get(url) as response:
        status = response.status
        body = await response.json()
    await session.close()
    assert expected_answer == {'status': status, 'length': body['hits']['total']['value']}
