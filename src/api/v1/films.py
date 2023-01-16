from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from models.api.film import FilmDescription, Film
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
        directors=film.directors
    )


@router.get('/films', response_model=list[Film])
async def films_main(params: str, film_service: FilmService = Depends(get_film_service)) -> list[Film]:
    films_list = await film_service.get_request(params)
