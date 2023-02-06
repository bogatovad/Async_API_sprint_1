from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Request

from api.v1.models.genre import GenreResponse
from core.messages import ErrorMessage
from services.genre import GenreService, get_genre_service

router = APIRouter()


@router.get(
    '/{genre_id}',
    response_model=GenreResponse,
    description='Получить информацию о жанре',
    response_description='Подробная информация о жанре'
)
async def genre_details(
        request: Request,
        genre_id: str,
        genre_service: GenreService = Depends(get_genre_service)
) -> GenreResponse:
    query_params = dict(
        genre_id=genre_id,
        request=request,
        index='genres'
    )
    genre = await genre_service.get_data_by_id(query_params)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=ErrorMessage.GENRE_NOT_FOUND)
    return GenreResponse(uuid=genre.id, name=genre.name)


@router.get(
    '/',
    response_model=list[GenreResponse],
    description='Список жанров',
    response_description='Список жанров'
)
async def list_genres(
        request: Request,
        genre_service: GenreService = Depends(get_genre_service)
) -> list[GenreResponse]:
    query_params = dict(
        request=request,
        index='genres'
    )
    genres = await genre_service.get_data_list(query_params)
    if not genres:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=ErrorMessage.GENRES_NOT_FOUND)
    return [GenreResponse(uuid=genre.id, name=genre.name) for genre in genres]
