import backoff
from elasticsearch import ConnectionError as ElasticConnectionError
from elasticsearch import Elasticsearch
from redis import Redis
from redis.exceptions import ConnectionError as RedisConnectionError
from settings import common_backoff_config, exception_es, exception_redis


@backoff.on_exception(
    **common_backoff_config,
    **exception_redis
)
def ping_redis():
    redis_client = Redis(
        host='redis',
        ssl=False,
        socket_connect_timeout=100
    )
    if redis_client.ping() is False:
        raise RedisConnectionError('Connect to redis is failed.')


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
    if es_client.ping() is False:
        raise ElasticConnectionError('Connect to elasticsearch is failed.')


if __name__ == '__main__':
    ping_redis()
    ping_es()
