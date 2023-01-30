from pydantic import BaseSettings, Field


class TestSettings(BaseSettings):
    ELASTIC_HOST: str = Field('host.docker.internal', env='ELASTIC_HOST')
    ELASTIC_PORT: str = Field('9200', env='ELASTIC_PORT')
    MOVIES_INDEX: str = 'movies'
    ES_ID_FIELD: str = 'id'
    REDIS_HOST: str = Field('127.0.0.1', env='REDIS_HOST')
    REDIS_PORT: str = Field('6379', env='REDIS_PORT')
    SERVICE_URL:  str = Field('127.0.0.1:8000')


test_settings = TestSettings()
