from pydantic import BaseSettings, Field


class TestSettings(BaseSettings):
    ES_HOST: str = Field('http://elasticsearch:9200/', env='ELASTIC_HOST')
    ES_INDEX: str = 'persons'
    ES_ID_FIELD: str = 'id'
    ES_INDEX_MAPPING: dict = {}

    REDIS_HOST: str = 'http://redis'
    SERVICE_URL: str = 'http://fastapi:8000/api/v1/'


test_settings = TestSettings()
