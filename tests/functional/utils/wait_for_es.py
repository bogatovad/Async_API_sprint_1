import time
import os, sys

# from tests.functional.settings import test_settings
from elasticsearch import Elasticsearch

if __name__ == '__main__':
    print('=' * 50, sys.path)
    es_client = Elasticsearch(hosts='http://localhost:9200', validate_cert=False, use_ssl=False)
    while True:
        if es_client.ping():
            break
        time.sleep(1)
