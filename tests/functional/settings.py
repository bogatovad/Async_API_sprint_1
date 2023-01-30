from pydantic import BaseSettings, Field


class TestSettings(BaseSettings):
    es_host: str = Field('http://elasticsearch:9200', env='ELASTIC_HOST')
    es_index: str = 'movies'
    es_id_field: str = 'id'
    es_index_mapping: dict = {}

    redis_host: str = 'http://redis'
    service_url: str = 'http://fastapi:8000'


test_settings = TestSettings()
