import backoff
from pydantic import BaseSettings, Field


backoff_config = {
    'wait_gen': backoff.expo,
    'exception': Exception,
    'max_tries': 3600,
    'raise_on_giveup': False
}


class TestSettings(BaseSettings):
    ES_HOST: str = Field('127.0.0.1', env='ELASTIC_HOST')
    ES_PORT: str = Field('9200', env='ELASTIC_PORT')
    MOVIES_INDEX: str = 'movies'
    ES_ID_FIELD: str = 'id'
    REDIS_HOST: str = Field('127.0.0.1', env='REDIS_HOST')
    REDIS_PORT: str = Field('6379', env='REDIS_PORT')
    SERVICE_URL:  str = Field('127.0.0.1:8000')


test_settings = TestSettings()
