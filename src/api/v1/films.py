from http import HTTPStatus
from typing import List, Union

from fastapi import APIRouter, Depends, HTTPException
from models.api.film import Film
from services.film import FilmService, get_film_service


router = APIRouter()


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
async def list_films(page: int, size: int, filter: Union[str, None] = None, sort: str = 'imdb_rating',
                     film_service: FilmService = Depends(get_film_service)) -> List[Film]:
    films = await film_service.get_all_films(sort, page, size, filter)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')
    return films

