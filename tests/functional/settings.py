from pydantic import BaseSettings, Field


class TestSettings(BaseSettings):
    # ELASTIC_HOST: str = Field('host.docker.internal', env='ELASTIC_HOST')
    # ELASTIC_PORT: str = Field('9200', env='ELASTIC_PORT')
    MOVIES_INDEX: str = 'movies'
    ES_ID_FIELD: str = 'id'
    REDIS_HOST: str = Field('http://redis', env='REDIS_HOST')
    REDIS_PORT: str = Field('6379', env='REDIS_PORT')
    SERVICE_URL:  str = Field('http://fastapi:8000')
    ELASTIC_HOST: str = Field('http://elasticsearch:9200', env='ELASTIC_HOST')
    ES_INDEX: str = 'movies'
    ES_INDEX_FIELD: str = 'id'
    ES_INDEX_MAPPING: dict = {}

    # REDIS_HOST: str = ''
    # SERVICE_URL: str = 'http://fastapi:8000'


test_settings = TestSettings()
