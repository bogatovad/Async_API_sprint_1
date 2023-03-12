from logging import config as logging_config

from pydantic import BaseSettings, Field

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):
    project_name: str = Field('movies', env='PROJECT_NAME')

    redis_host: str = Field('redis', env='REDIS_HOST')
    redis_port: int = Field(6379, env='REDIS_PORT')

    elastic_host: str = Field('elasticsearch', env='ELASTIC_HOST')
    elastic_port: int = Field(9200, env='ELASTIC_PORT')

    fastapi_host: str = Field("0.0.0.0", env="FASTAPI_HOST")
    fastapi_port: int = Field(8000, env="FASTAPI_PORT")

    auth_host: str = Field("127.0.0.1", env="AUTH_HOST")
    auth_port: int = Field(80, env="AUTH_PORT")

    film_cache_expire_in_seconds: int = 60 * 5
    genre_cache_expire_in_seconds: int = 60 * 5
    person_cache_expire_in_seconds: int = 60 * 5

    class Config:
        env_file = "envs/.env"


settings = Settings()
