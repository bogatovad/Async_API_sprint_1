import backoff
import time

from redis import Redis, ConnectionError

import settings

#@backoff.on_exception(**backoff_config)
def ping_redis():
    redis_client = Redis(
        host='redis',
        ssl=False,
        socket_connect_timeout=5
    )
    while True:
        if redis_client.ping():
            return
        time.sleep(2)


if __name__ == '__main__':
    ping_redis()