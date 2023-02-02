#!make

include envs/.env
BASE_COMMAND = docker-compose run --rm
COMMAND = ${BASE_COMMAND}  /bin/bash -c
COMPOSE = docker-compose
DOCKER_COMPOSE_CMD=docker-compose
DOCKER_COMPOSE_DIR=`pwd`
COMPOSE_TEST_FILE = tests/functional/docker-compose.yml

build:
	${COMPOSE} build

start:
	${COMPOSE} start

stop:
	${COMPOSE} stop

up:
	${COMPOSE} up

down:
	${COMPOSE} down

flake8:
	${BASE_COMMAND} fastapi flake8

isort:
	${BASE_COMMAND} fastapi isort ./

fastapi-bash:
	${BASE_COMMAND} fastapi /bin/bash

test:
	cd tests/functional && docker-compose down && docker-compose build && docker-compose up --exit-code-from tests
