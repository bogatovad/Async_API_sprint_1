FROM python:3.10.8-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

WORKDIR /functional
RUN groupadd -r tests && useradd -d /functional -r -g tests tests

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
RUN chown tests:tests -R /functional

USER tests
