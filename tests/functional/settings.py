from pydantic import BaseSettings, Field


class TestSettings(BaseSettings):
    es_host: str = Field('http://127.0.0.1:9200', env='ELASTIC_HOST')
    es_index: str # TODO to fill
    es_id_field: str # TODO to fill
    es_index_mapping: dict # TODO to fill

    redis_host: str # TODO to fill
    service_url: str # TODO to fill


test_settings = TestSettings()
