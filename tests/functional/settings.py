from pydantic import BaseSettings, Field


class TestSettings(BaseSettings):
    es_host: str = Field('http://127.0.0.1', env='ELASTIC_HOST')
    es_port: int = Field(9200, env='ELASTIC_PORT')
    redis_host: str = Field('http://127.0.0.1', env='REDIS_HOST')
    redis_port: int = Field(6379, env='REDIS_PORT')
    fastapi_host: str = Field('http://127.0.0.1', env='FASTAPI_HOST')
    fastapi_port: int = Field(8000, env='FASTAPI_PORT')

    #es_index: str # TODO to fill
    #es_id_field: str # TODO to fill
    #es_index_mapping: dict # TODO to fill


test_settings = TestSettings()
