import pytest
from elasticsearch import AsyncElasticsearch
from settings import test_settings
import json
import uuid
import datetime


@pytest.fixture
async def get_es_bulk_query(data, es_index=test_settings.es_index, es_id_field=test_settings.es_id_field) -> list:
    es_data = [{
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
    } for _ in range(60)]

    bulk_query = []
    for row in es_data:
        bulk_query.extend([
            json.dumps({'index': {'_index': test_settings.es_index, '_id': row[test_settings.es_id_field]}}),
            json.dumps(row)
        ])
    return bulk_query


@pytest.fixture
def es_write_data():
    async def inner(data: list[dict]):

        bulk_query = await get_es_bulk_query(data, test_settings.es_index, test_settings.es_id_field)
        str_query = '\n'.join(bulk_query) + '\n'

        es_client = AsyncElasticsearch(
            hosts=test_settings.es_host, validate_cert=False, use_ssl=False
        )
        response = await es_client.bulk(str_query, refresh=True)
        await es_client.close()
        if response['errors']:
            raise Exception('Ошибка записи данных в Elasticsearch')
    return inner
