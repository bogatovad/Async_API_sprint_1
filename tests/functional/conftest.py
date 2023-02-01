import datetime
import json
import uuid

import pytest
import requests
from elasticsearch import AsyncElasticsearch

from .settings import test_settings


@pytest.fixture
async def es_client():
    client = AsyncElasticsearch(hosts='http://elasticsearch:9200')
    yield client
    await client.close()
    requests.delete('http://elasticsearch:9200/movies')
    requests.delete('http://elasticsearch:9200/persons')


def get_es_bulk_query(es_data, es_index, es_id_field):
    bulk_query = []
    for row in es_data:
        bulk_query.extend([
            json.dumps({'index': {'_index': es_index, '_id': row[es_id_field]}}),
            json.dumps(row)
        ])
    return '\n'.join(bulk_query) + '\n'


@pytest.fixture
def es_write_data(es_client):
    async def inner(data: list[dict], es_index: str):
        bulk_query = get_es_bulk_query(data, es_index, test_settings.ES_ID_FIELD)
        response = await es_client.bulk(bulk_query, refresh=True)
        await es_client.close()
        if response['errors']:
            raise Exception(f'Ошибка записи данных в Elasticsearch')
    return inner


def generate_es_data_person():
    return [
        {
            'id': str(uuid.uuid4()),
            'full_name': 'Petr Ivanov',
        }
        for _ in range(60)
    ]


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
                {'id': '222', 'name': 'Bob'},
                # {'id': '44', 'name': 'Petr Ivanov'}

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


def generate_single_film():
    return [
        {
            'id': str('12bb1b7e-b039-4f66-9248-b35d795e38f6'),
            'imdb_rating': 8.5,
            'genre': ['Action', 'Sci-Fi'],
            'title': 'The Star',
            'description': 'New World',
            'director': ['Stan'],
            'actors_names': ['Ann', 'Bob'],
            'writers_names': ['Ben', 'Howard'],
            'actors': [
                {'id': '111', 'name': 'Ann'},
                {'id': '222', 'name': 'Bob'},

            ],
            'writers': [
                {'id': '333', 'name': 'Ben'},
                {'id': '444', 'name': 'Howard'}
            ],
        }
    ]
