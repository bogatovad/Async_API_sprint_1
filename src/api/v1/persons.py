from http import HTTPStatus
from typing import List

from api.v1.models.film import FilmResponse
from api.v1.models.person import PersonDescriptionResponse
from fastapi import APIRouter, Depends, HTTPException, Request
from services.person import PersonService, get_person_service

router = APIRouter()


@router.get(
    '/search',
    response_model=List[PersonDescriptionResponse],
    description='Поиск по персоне',
    response_description='Результат поиска'
)
async def search_persons(request: Request, person_service: PersonService = Depends(get_person_service))\
        -> List[PersonDescriptionResponse]:
    query_params = dict(request.query_params)
    persons = await person_service.search_persons(query_params)
    if not persons:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='films with person not found')
    return [
        PersonDescriptionResponse(
            uuid=person.id,
            role=person.role,
            film_ids=person.film_ids,
            name=person.full_name
        )
        for person in persons
    ]


@router.get(
    '/{person_id}',
    response_model=PersonDescriptionResponse,
    description='Получить информацию о персоне',
    response_description='Подробная информация о персоне'
)
async def person_details(
        person_id: str, person_service: PersonService = Depends(get_person_service)
) -> PersonDescriptionResponse:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')
    return PersonDescriptionResponse(uuid=person.id, role=person.role, film_ids=person.film_ids, name=person.full_name)


@router.get(
    '/{person_id}/film',
    response_model=List[FilmResponse],
    description='Получить фильмы по персоне.',
    response_description='Фильмы по персоне.'

)
async def list_film_by_person(
        person_id: str,
        person_service: PersonService = Depends(get_person_service)
) -> List[FilmResponse]:
    films = await person_service.get_film_by_id(person_id)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='films with person not found')
    return [FilmResponse(uuid=film.id, title=film.title, imdb_rating=film.imdb_rating) for film in films]
