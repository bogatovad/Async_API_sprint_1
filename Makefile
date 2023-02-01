#!make

include envs/.env
BASE_COMMAND = docker-compose run --rm
COMMAND = ${BASE_COMMAND}  /bin/bash -c
COMPOSE = docker-compose
DOCKER_COMPOSE_CMD=docker-compose
DOCKER_COMPOSE_DIR=`pwd`
COMPOSE_TEST_FILE = /home/artem/Документы/учеба/Async_API_sprint_1/tests/functional

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

test_build:
	${DOCKER_COMPOSE_CMD} build -f ${COMPOSE_TEST_FILE}

test_up:
	${DOCKER_COMPOSE_CMD} up -f ${COMPOSE_TEST_FILE} --exit-code-from tests

run_tests: test_build
