from redis import Redis
from settings import test_settings
import time

if __name__ == '__main__':
    redis_client = Redis(host=test_settings.REDIS_HOST, port=test_settings.REDIS_PORT)
    while True:
        if redis_client.ping():
            break
        time.sleep(1)
