import backoff
from pydantic import BaseSettings, Field


backoff_config = {
    'wait_gen': backoff.expo,
    'exception': Exception,
    'max_tries': 3600,
    'raise_on_giveup': False
}


class TestSettings(BaseSettings):
    es_host: str = Field('http://elasticsearch:9200/', env='elastic_host')
    es_person_index: str = 'persons'
    es_movies_index: str = 'movies'
    es_id_field: str = 'id'
    es_index_mapping: dict = {}

    redis_host: str = Field('http://redis', env='redis_host')
    service_url: str = Field('http://fastapi:8000/api/v1/', env='SERVICE_URL')


test_settings = TestSettings()
