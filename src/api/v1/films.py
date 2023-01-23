from http import HTTPStatus
from typing import List, Optional

from fastapi import Query

from fastapi import Path

from core.messages import ErrorMessage
from api.v1.models.film import FilmDescriptionResponse, FilmResponse

from fastapi import APIRouter, Depends, HTTPException
from services.film import FilmService, get_film_service

router = APIRouter()


@router.get(
    '/search',
    response_model=List[FilmResponse],
    description='Главная страница',
    response_description='Список фильмов на главной странице'
)
async def search_films(
        page_size: Optional[int] = Query(1, alias='page[size]', description='Items amount on page', ge=1),
        page_number: Optional[int] = Query(10, alias='page[number]', description='Page number for pagination', ge=1),
        query: Optional[str] = Query('', description='Search string for query.'),
        sort: Optional[str] = Query('imdb_rating', description='Field for sorting.'),
        film_service: FilmService = Depends(get_film_service)) -> List[FilmResponse]:
    query_params = dict(
        page_size=page_size,
        page_number=page_number,
        query=query,
        sort=sort
    )
    films = await film_service.get_search(query_params)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')
    return [FilmResponse(uuid=film.id, title=film.title, imdb_rating=film.imdb_rating) for film in films]


@router.get(
    '/{film_id}',
    response_model=FilmDescriptionResponse,
    description='Получить информацию о фильме',
    response_description='Подробная информация о фильме'
)
async def film_details(film_id: str, film_service: FilmService = Depends(get_film_service)) -> FilmDescriptionResponse:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=ErrorMessage.FILM_NOT_FOUND)
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
    '/',
    response_model=list[FilmResponse],
    description='Главная страница',
    response_description='Список фильмов на главной странице'
)
async def list_films(
     page_size: Optional[int] = Query(1, alias='page[size]', description='Items amount on page', ge=1),
     page_number: Optional[int] = Query(10, alias='page[number]', description='Page number for pagination', ge=1),
     sort: Optional[str] = Query('imdb_rating', description='Field for sorting.'),
     filter_genre: Optional[str] = Query('',  alias="filter[genre]", description='Field for filtering.'),
     film_service: FilmService = Depends(get_film_service),
 ) -> List[FilmResponse]:
    query_params = dict(
        page_size=page_size,
        page_number=page_number,
        sort=sort
    )
    query_params['filter[genre]'] = filter_genre
    films = await film_service.get_all_films(query_params)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=ErrorMessage.FILM_NOT_FOUND)
    return [FilmResponse(uuid=film.id, title=film.title, imdb_rating=film.imdb_rating) for film in films]


@router.get(
    '/alike/{film_id}',
    response_model=list[FilmResponse],
    description='Похожие фильмы',
    response_description='Список похожих фильмов'
)
async def films_alike(
        film_id: str = Path(None, description='id фильма, для которого ищем похожие'),
        film_service: FilmService = Depends(get_film_service)
) -> list[FilmResponse]:
    films = await film_service.get_films_alike(film_id)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=ErrorMessage.FILM_NOT_FOUND)
    return [FilmResponse(uuid=film.id, title=film.title, imdb_rating=film.imdb_rating) for film in films]
