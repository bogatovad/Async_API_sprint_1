from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from models.api.genre import Genre
from services.film import GenreService, get_genre_service

router = APIRouter()


@router.get(
    '/{genre_id}',
    response_model=Genre,
    description='Получить информацию о жанре',
    response_description='Подробная информация о жанре'
)
async def genre_details(genre_id: str, genre_service: GenreService = Depends(get_genre_service)) -> Genre:
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='genres not found')
    return genre


@router.get(
    '/',
    response_model=List[Genre],
    description='Список жанров',
    response_description='Список жанров'
)
async def list_genres(genre_service: GenreService = Depends(get_genre_service)) -> List[Genre]:
    genres = await genre_service.get_list()
    if not genres:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='genres not found')
    return genres
