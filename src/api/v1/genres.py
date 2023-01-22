from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from core.messages import ErrorResponse
from models.api.genre import GenreResponse
from services.genre import GenreService, get_genre_service

router = APIRouter()


@router.get(
    '/{genre_id}',
    response_model=GenreResponse,
    description='Получить информацию о жанре',
    response_description='Подробная информация о жанре'
)
async def genre_details(genre_id: str, genre_service: GenreService = Depends(get_genre_service)) -> GenreResponse:
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=ErrorResponse.GENRE_NOT_FOUND)
    return GenreResponse(uuid=genre.id, name=genre.name)


@router.get(
    '/',
    response_model=list[GenreResponse],
    description='Список жанров',
    response_description='Список жанров'
)
async def list_genres(genre_service: GenreService = Depends(get_genre_service)) -> list[GenreResponse]:
    genres = await genre_service.get_list()
    if not genres:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=ErrorResponse.GENRES_NOT_FOUND)
    return [GenreResponse(uuid=genre.id, name=genre.name) for genre in genres]
