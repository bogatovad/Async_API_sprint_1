import backoff
import time

from redis import Redis
from elasticsearch import Elasticsearch

from settings import test_settings, backoff_config


@backoff.on_exception(**backoff_config)
def ping_redis():
    redis_client = Redis(
        '127.0.0.1',
        ssl=False,
        socket_connect_timeout=5
    )
    while True:
        if redis_client.ping():
            break
        time.sleep(20)


def ping_es():
    es_client = Elasticsearch('http://127.0.0.1:9200', 
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
