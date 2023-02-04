import backoff
import time

from redis import Redis, ConnectionError


#@backoff.on_exception(**backoff_config)
def ping_redis():
    redis_client = Redis(
        host='http://redis',
        ssl=False,
        socket_connect_timeout=5
    )
    while True:
        try:
            if redis_client.ping():
                return
        except ConnectionError:
            time.sleep(2)


if __name__ == '__main__':
    ping_redis()