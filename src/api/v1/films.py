from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from models.api.film import Film, FilmDescription
from services.film import FilmService, get_film_service

router = APIRouter()
MOCK_PERSON = {'id': '123', 'full_name': 'full_name'}
MOCK_GENRE = {'id': '1', 'name': 'genre'}
MOCK_FILM_DESCRIPTION = {'id': 1, 'title': 'title', 'imdb_rating': 10, 'description': 'description', 'genre': [MOCK_GENRE], 'actors': [MOCK_PERSON], 'writers': [MOCK_PERSON], 'directors': [MOCK_PERSON]}
MOCK_FILM = {'id': 1, 'title': 'title', 'imdb_rating': 10}


@router.get(
    '/{film_id}',
    response_model=FilmDescription,
    description='Получить информацию о фильме',
    response_description='Подробная информация о фильме'
)
async def film_details(film_id: str, film_service: FilmService = Depends(get_film_service)) -> FilmDescription:
    film = await film_service.get_by_id(film_id)
    film = True# TODO: REMOVE MOCK!!!
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')
    return FilmDescription(**MOCK_FILM_DESCRIPTION)


@router.get(
    '/',
    response_model=List[Film],
    response_description='Список фильмов'
)
async def film_list(
    page_size: int = Query(10, description='Количество фильмов на странице'),
    page: int = Query(1, description='Номер страницы'),
    film_service: FilmService = Depends(get_film_service)
) -> List[Film]:
    film = await film_service.get_all()
    return [Film(**MOCK_FILM)]
