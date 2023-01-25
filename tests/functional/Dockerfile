FROM python:3.10.8-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /tests

COPY entrypoint.sh entrypoint.sh
COPY requirements.txt requirements.txt

RUN chmod +x 'entrypoint.sh' \
&& pip install --upgrade pip \
&& pip install -r requirements.txt \
&& groupadd -r tests && useradd -d /tests -r -g tests tests\
&& chown tests:tests -R /tests

COPY . .

USER tests

ENTRYPOINT ["./entrypoint.sh"]
