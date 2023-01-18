from http import HTTPStatus
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from models.api.film import Film, FilmDescription
from services.film import FilmService, get_film_service

router = APIRouter()


@router.get('/{film_id}', response_model=FilmDescription)
async def film_details(film_id: str, film_service: FilmService = Depends(get_film_service)) -> FilmDescription:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')

    return FilmDescription(
        id=film.id,
        title=film.title,
        imdb_rating=film.imdb_rating,
        description=film.description,
        genre=film.genre,
        actors=film.actors,
        writers=film.writers,
        directors=film.director
    )


@router.get('/', response_model=List[Film])
async def films_main(request: Request, film_service: FilmService = Depends(get_film_service)):
    films_list = await film_service.get_all_films()
    result = []
    for movie in films_list['hits']['hits']:
        result.append(film_service.model(**movie['_source']))
    return result


@router.get('/search', response_model=Optional[Film, List[Film]])
async def films_main(request: Request, film_service: FilmService = Depends(get_film_service)):
    query_params = (dict(request.query_params))
    films_list = await film_service.get_search(query_params)
    result = []
    for movie in films_list['hits']['hits']:
        result.append(film_service.model(**movie['_source']))
    return result