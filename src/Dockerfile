# Выбор версии 3.8 обусловлен нормльной установкой для данного образа uvloop и orjson
FROM python:3.8-slim

RUN pip install --upgrade pip

WORKDIR /fastapi
RUN groupadd -r fastapi && useradd -d /fastapi -r -g fastapi fastapi

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
RUN chown fastapi:fastapi -R /fastapi
RUN chmod +x ./wait-for-it.sh

USER fastapi
CMD ./wait-for-it.sh ${REDIS_HOST}:${REDIS_PORT} && python3 main.py