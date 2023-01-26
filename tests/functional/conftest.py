import pytest
from elasticsearch import AsyncElasticsearch
from .settings import test_settings
import json


@pytest.fixture(scope='session')
async def es_client():
    client = AsyncElasticsearch(hosts='http://elasticsearch:9200')
    yield client
    await client.close()


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
    async def inner(data: list[dict]):
        bulk_query = get_es_bulk_query(data, test_settings.es_index, test_settings.es_id_field)
        response = await es_client.bulk(bulk_query, refresh=True)
        print(f'RESPONSE = {response=}')
        await es_client.close()
        if response['errors']:
            raise Exception('Ошибка записи данных в Elasticsearch')
    return inner
