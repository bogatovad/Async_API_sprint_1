#!make

include .env
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
	${BASE_COMMAND} fasttapi isort ./