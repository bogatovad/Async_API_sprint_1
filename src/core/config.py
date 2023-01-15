import os
from logging import config as logging_config

from environs import Env
from .logger import LOGGING

env = Env()
env.read_env()

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)

# Название проекта. Используется в Swagger-документации
PROJECT_NAME = env('PROJECT_NAME', 'movies')

# Настройки Redis
REDIS_HOST = env('REDIS_HOST', '127.0.0.1')
REDIS_PORT = env('REDIS_PORT', 6379)

# Настройки Elasticsearch
ELASTIC_HOST = env('ELASTIC_HOST', '127.0.0.1')
ELASTIC_PORT = env('ELASTIC_PORT', 9200)

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
