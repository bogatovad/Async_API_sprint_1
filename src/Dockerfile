FROM python:3.10.8-slim-bullseye

RUN pip install --upgrade pip

WORKDIR /fastapi
RUN mkdir /fastapi/tests
RUN groupadd -r fastapi && useradd -d /fastapi -r -g fastapi fastapi

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
RUN chown fastapi:fastapi -R /fastapi
RUN chmod +x ./wait-for-it.sh

USER fastapi
CMD python3 main.py