from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from models.api.film import FilmDescriptionResponse, FilmResponse
from services.film import FilmService, get_film_service

router = APIRouter()


@router.get(
    '/{film_id}',
    response_model=FilmDescriptionResponse,
    description='Получить информацию о фильме',
    response_description='Подробная информация о фильме'
)
async def film_details(film_id: str, film_service: FilmService = Depends(get_film_service)) -> FilmDescriptionResponse:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')
    return film


@router.get(
    '/',
    response_model=List[FilmResponse],
    description='Главная страница',
    response_description='Список фильмов на главной странице'
)
async def film_list(
    page_size: int = Query(10, description='Количество фильмов на странице'),
    page: int = Query(1, description='Номер страницы'),
    film_service: FilmService = Depends(get_film_service)
) -> List[FilmResponse]:
    films_list = await film_service.get_all()
    return films_list
