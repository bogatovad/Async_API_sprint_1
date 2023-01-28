import backoff
import time

from redis import Redis
from elasticsearch import Elasticsearch

from settings import test_settings, backoff_config


@backoff.on_exception(**backoff_config)
def ping_redis():
    redis_client = Redis(
        host=test_settings.REDIS_HOST,
        ssl=False,
        socket_connect_timeout=5
    )
    while True:
        if redis_client.ping():
            break
        time.sleep(1)


@backoff.on_exception(**backoff_config)
def ping_es():
    es_client =Elasticsearch(f'http://{test_settings.ELASIC_HOST}:{test_settings.ELASTIC_PORT}', 
        validate_cert=False,
        use_ssl=False
    )
    while True:
        if es_client.ping():
            break
        time.sleep(1)


if __name__ == '__main__':
    ping_redis()
    ping_es()
