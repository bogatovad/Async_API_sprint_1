FROM python:3.10.8-bullseye

RUN pip install --upgrade pip

WORKDIR /fastapi
RUN groupadd -r fastapi && useradd -d /fastapi -r -g fastapi fastapi

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN apt update && apt install netcat -y

COPY . .
RUN chown fastapi:fastapi -R /fastapi
RUN chmod +x ./wait-for-it.sh

USER fastapi
CMD ./wait-for-it.sh ${REDIS_HOST}:${REDIS_PORT} && python3 main.py