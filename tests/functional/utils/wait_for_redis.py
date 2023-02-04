import backoff
import time

from redis import Redis

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
            return
        time.sleep(1)


if __name__ == '__main__':
    ping_redis()