import os
from logging import config as logging_config

from environs import Env
from pydantic import BaseSettings

from core.logger import LOGGING

env = Env()
env.read_env()

logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):
    PROJECT_NAME: str = env('PROJECT_NAME', 'movies')

    REDIS_HOST: str = env('REDIS_HOST', 'redis')
    REDIS_PORT: int = env.int('REDIS_PORT', 6379)

    ELASTIC_HOST: str = env('ELASTIC_HOST', 'elasticsearch')
    ELASTIC_PORT: int = env.int('ELASTIC_PORT', 9200)

    FASTAPI_HOST: str = env("FASTAPI_HOST", "0.0.0.0")
    FASTAPI_PORT: int = env.int("FASTAPI_PORT", 8000)

    FILM_CACHE_EXPIRE_IN_SECONDS: int = 60 * 5
    GENRE_CACHE_EXPIRE_IN_SECONDS: int = 60 * 5
    PERSON_CACHE_EXPIRE_IN_SECONDS: int = 60 * 5

    class Config:
        BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        env_file = os.path.join(BASE_DIR, 'enviromens/.env')


settings = Settings()
