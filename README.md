# Проектное задание: Async_API_sprint_1
Асинхронный API для кинотеатра. Этот сервис - точка входа для всех клиентов. В этой итерации в сервисе только анонимные пользователи.

Авторы:
 - [bogatovad](https://github.com/bogatovad)
 - [acetone415](https://github.com/acetone415)
 - [Seniacat](https://github.com/Seniacat)

## Используемые технологии
 - Код приложения пишется на Python + FastAPI.
 - Приложение запускается под управлением сервера ASGI(uvicorn).
 - В качестве хранилища используется ElasticSearch.
 - Для кеширования данных понадобится Redis Cluster.
 - Все компоненты системы запускаются через Docker.


## Запуск
Создать и заполнить .env из .env.example в папке `Async_API_sprint_1/envs`.
Из этой же папки выполнить:
```
make build
make up
```
## Запуск тестов

из директории tests/functional выполнить команду

```
docker-compose down && docker-compose build && docker-compose up --exit-code-from tests
```

## Линтинг и сортировка импортов
Для запуска линтера python-проекта выполните следующую команду в корневой папке проекта:
```
make flake8
```
Сортировка импортов
```
make isort
```

## Ссылки на сервисы

1. https://github.com/bogatovad/Async_API_sprint_1
2. https://github.com/bogatovad/new_admin_panel_sprint_3


## API сервисы

 - Полный список фильмов: http://localhost:8000/api/v1/films/
 - Фильм по UUID: http://localhost:8000/api/v1/film/film_uuid/
 - Похожие фильмы: http://localhost:8000/api/v1/films/alike/film_uuid/
 - Поиск по фильмам: http://localhost:8000/api/v1/film/search/
 - Информация о киноперсоне по UUID: http://localhost:8000/api/v1/person/person_uuid/
 - Поиск по киноперсонам: http://localhost:8000/api/v1/person/search/
 - Получить фильмы по персоне - http://localhost:8000/api/v1/person/person_uuid/film/
 - Список жанров: http://localhost:8000/api/v1/genre/
 - Информация по жанру: http://localhost:8000/api/v1/genre/genre_uuid/


## Документация API
Доступна по адресу `http://{FASTAPI_HOST}:{FASTAPI_PORT}/api/openapi`
