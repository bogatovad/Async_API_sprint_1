import os
from logging import config as logging_config

from environs import Env

from core.logger import LOGGING

env = Env()
env.read_env()

logging_config.dictConfig(LOGGING)

PROJECT_NAME = env('PROJECT_NAME', 'movies')

REDIS_HOST = env('REDIS_HOST', 'redis')
REDIS_PORT = env('REDIS_PORT', 6379)

ELASTIC_HOST = env('ELASTIC_HOST', 'elasticsearch')
ELASTIC_PORT = env('ELASTIC_PORT', 9200)

FASTAPI_HOST = env("FASTAPI_HOST", "0.0.0.0")
FASTAPI_PORT = env("FASTAPI_PORT", 8000)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5
