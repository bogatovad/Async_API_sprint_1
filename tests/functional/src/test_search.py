import aiohttp
import pytest

from elasticsearch import AsyncElasticsearch

from functional.settings import test_settings


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'search': 'The Star'},
                {'status': 200, 'length': 50}
        ),
        (
                {'search': 'Mashed potato'},
                {'status': 200, 'length': 0}
        )
    ]
)
@pytest.mark.asyncio
async def test_search(es_write_data, get_es_bulk_query, query_data, expected_answer):

    bulk_query = get_es_bulk_query
    str_query = '\n'.join(bulk_query) + '\n'
    es_client = AsyncElasticsearch(hosts=test_settings.ES_HOST,
                                   validate_cert=False,
                                   use_ssl=False)
    response = await es_client.bulk(str_query, refresh=True)
    await es_client.close()
    # if response['errors']:
    #     print(response['errors'])
    #     raise Exception('Ошибка записи данных в Elasticsearch')

    session = aiohttp.ClientSession()
    url = test_settings.SERVICE_URL + '/api/v1/search'
    query_data = {'search': 'The Star'}
    async with session.get(url, params=query_data) as response:
        body = await response.json()
        headers = response.headers
        status = response.status
    await session.close()

    assert status == 200
    assert len(response.body) == 50