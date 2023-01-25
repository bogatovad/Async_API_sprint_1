FROM python:3.10.8-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /tests
RUN groupadd -r tests && useradd -d /tests -r -g tests tests

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip \
&& pip install -r requirements.txt

COPY entrypoint.sh .
COPY ./ ./tests