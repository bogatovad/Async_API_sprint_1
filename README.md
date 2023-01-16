## Запуск
Создать и заполнить .env из .env.example в папке `Async_API_sprint_1/enviroments`.  
Из этой же папки выполнить:
```
make build
make up
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

## Документация API
Доступна по адресу `http://{FASTAPI_HOST}:{FASTAPI_PORT}/api/openapi`