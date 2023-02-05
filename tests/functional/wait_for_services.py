from datetime import time

import backoff
from elasticsearch import Elasticsearch
from redis import Redis
from settings import common_backoff_config, exception_es, exception_redis


@backoff.on_exception(
    **common_backoff_config,
    **exception_redis
)
def ping_redis():
    redis_client = Redis(
        host='redis',
        ssl=False,
        socket_connect_timeout=5
    )
    if redis_client.ping():
        return


@backoff.on_exception(
    **common_backoff_config,
    **exception_es,
)
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
