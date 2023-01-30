FROM python:3.10.8-slim-bullseye

RUN pip install --upgrade pip

WORKDIR /functional
RUN groupadd -r tests && useradd -d /functional -r -g tests tests

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
RUN chown tests:tests -R /functional

USER tests
CMD python3 utils/wait_for_es.py && python3 utils/wait_for_redis.py && pytest src