#!make

include envs/.env
BASE_COMMAND = docker-compose run --rm
COMMAND = ${BASE_COMMAND}  /bin/bash -c
COMPOSE = docker-compose

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

tests-build:
	docker-compose -f tests/functional/docker-compose.yml build

tests-up:
	docker-compose -f tests/functional/docker-compose.yml up

tests-down:
	docker-compose -f tests/functional/docker-compose.yml down
