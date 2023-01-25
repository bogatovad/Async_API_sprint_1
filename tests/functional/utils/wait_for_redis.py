import time

from redis import Redis

from settings import test_settings


if __name__ == '__main__':
    redis_client = Redis(
        test_settings.redis_host,
        ssl=False,
        socket_connect_timeout=5
    )
    while True:
        if redis_client.ping():
            break
        time.sleep(1)
