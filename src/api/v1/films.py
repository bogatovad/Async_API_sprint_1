from http import HTTPStatus
from typing import List

from fastapi import Request
from fastapi import APIRouter, Depends, HTTPException, Path
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
    return FilmDescriptionResponse(
        uuid=film.id,
        title=film.title,
        imdb_rating=film.imdb_rating,
        description=film.description,
        genre=film.genre,
        actors=film.actors,
        writers=film.writers,
        directors=film.director
    )


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
    return FilmDescriptionResponse(
        uuid=film.id, title=film.title, imdb_rating=film.imdb_rating, description=film.description,
        genre=film.genre, actors=film.actors, writers=film.writers, directors=film.director
    )


@router.get(
    '/',
    response_model=List[FilmResponse],
    description='Главная страница',
    response_description='Список фильмов на главной странице'
)
async def list_films(request: Request, film_service: FilmService = Depends(get_film_service)) -> List[FilmResponse]:
    query_params = dict(request.query_params)
    films = await film_service.get_all_films(query_params)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')
    return [FilmResponse(uuid=film.id, title=film.title, imdb_rating=film.imdb_rating) for film in films]


@router.get(
    '/alike/{film_id}',
    response_model=List[FilmResponse],
    description='Похожие фильмы',
    response_description='Список похожих фильмов'
)
async def films_alike(
        film_id: str = Path(None, description='id фильма, для которого ищем похожие'),
        film_service: FilmService = Depends(get_film_service)
) -> List[FilmResponse]:
    films = await film_service.get_films_alike(film_id)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')
    return [FilmResponse(uuid=film.id, title=film.title, imdb_rating=film.imdb_rating) for film in films]
