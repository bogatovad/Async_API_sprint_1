from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request
from models.api.film import Film
from services.film import FilmService, get_film_service

router = APIRouter()


@router.get(
    '/search',
    response_model=List[Film],
    description='Поиск по фильмам',
    response_description='Результат поиска'
)
async def search_movies(request: Request, film_service: FilmService = Depends(get_film_service)) -> List[Film]:
    query_params = dict(request.query_params)
    films = await film_service.get_search(query_params)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='films not found')
    return films


@router.get(
    '/{film_id}',
    response_model=Film,
    description='Получить информацию о фильме',
    response_description='Подробная информация о фильме'
)
async def film_details(film_id: str, film_service: FilmService = Depends(get_film_service)) -> Film:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')
    return Film(id=film.id, title=film.title)


@router.get(
    '/',
    response_model=List[Film],
    description='Главная страница',
    response_description='Список фильмов на главной странице'
)
async def list_films(request: Request, film_service: FilmService = Depends(get_film_service)) -> List[Film]:
    query_params = dict(request.query_params)
    films = await film_service.get_all_films(query_params)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')
    return films
