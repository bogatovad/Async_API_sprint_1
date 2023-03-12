from http import HTTPStatus
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query, Request

from api.v1.common_paramaters import paginated_params
from api.v1.models.film import FilmDescriptionResponse, FilmResponse
from core.messages import ErrorMessage
from services.film import FilmService, get_film_service
from services.auth import special_permissions

router = APIRouter()


@router.get(
    '/search',
    response_model=List[FilmResponse],
    description='Главная страница',
    response_description='Список фильмов на главной странице'
)
async def search_films(
        request: Request,
        common: dict = Depends(paginated_params),
        query: Optional[str] = Query('', description='Search string for query.'),
        sort: Optional[str] = Query('imdb_rating', description='Field for sorting.'),
        film_service: FilmService = Depends(get_film_service)) -> List[FilmResponse]:
    query_params = dict(
        **common,
        query=query,
        sort=sort,
        request=request,
        index='movies'
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
@special_permissions(['subscriber', 'admin'])
async def film_details(
        request: Request,
        film_id: str,
        film_service: FilmService = Depends(get_film_service)
) -> FilmDescriptionResponse:
    print(request)
    query_params = dict(
        film_id=film_id,
        request=request,
        index='movies'
    )
    film = await film_service.get_data_by_id(query_params)
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
    request: Request,
    common: dict = Depends(paginated_params),
    sort: Optional[str] = Query('imdb_rating', description='Field for sorting.'),
    filter_genre: Optional[str] = Query('',  alias="filter[genre]", description='Field for filtering.'),
    film_service: FilmService = Depends(get_film_service)
) -> List[FilmResponse]:
    query_params = dict(
        **common,
        sort=sort,
        request=request,
        index='movies'
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
        request: Request,
        film_id: str = Path(None, description='id фильма, для которого ищем похожие'),
        film_service: FilmService = Depends(get_film_service)
) -> list[FilmResponse]:
    query_params = dict(
        film_id=film_id,
        request=request,
        index='movies'
    )
    films = await film_service.get_films_alike(query_params)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=ErrorMessage.FILM_NOT_FOUND)
    return [
        FilmResponse(
            uuid=film.id,
            title=film.title,
            imdb_rating=film.imdb_rating
        )
        for film in films
    ]
