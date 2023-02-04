import backoff
from pydantic import BaseSettings, Field


backoff_config = {
    'wait_gen': backoff.expo,
    'exception': Exception,
    'max_tries': 3600,
    'raise_on_giveup': False
}


class TestSettings(BaseSettings):
    ES_HOST: str = Field('http://elasticsearch:9200/', env='ELASTIC_HOST')
    ES_PERSONS_INDEX: str = 'persons'
    ES_MOVIES_INDEX: str = 'movies'
    ES_ID_FIELD: str = 'id'
    ES_INDEX_MAPPING: dict = {}

    REDIS_HOST: str = 'redis'
    SERVICE_URL: str = 'http://fastapi:8000/api/v1/'


test_settings = TestSettings()
