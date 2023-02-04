import backoff
import time
from elasticsearch import Elasticsearch
from redis import Redis
from settings import backoff_config


@backoff.on_exception(**backoff_config)
def ping_redis():
    redis_client = Redis(
        host='redis',
        ssl=False,
        socket_connect_timeout=5
    )
    redis_client.ping()


@backoff.on_exception(**backoff_config)
def ping_es():
    es_client = Elasticsearch(
        hosts='http://elasticsearch:9200/',
        validate_cert=False,
        use_ssl=False
    )
    es_client.ping()


if __name__ == '__main__':
    ping_redis()
    ping_es()