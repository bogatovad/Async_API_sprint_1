#!/bin/bash

python3 pip install -r /tests/functional/requirements.txt
python3 /tests/functional/utils/wait_for_es.py
python3 /tests/functional/utils/wait_for_redis.py
pytest /tests/functional/src