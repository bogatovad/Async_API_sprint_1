from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from models.api.film import FilmResponse
from models.api.person import PersonDescription
from services.film import PersonService, get_person_service

router = APIRouter()


@router.get(
    '/search',
    response_model=List[PersonDescription],
    description='Поиск по персоне',
    response_description='Результат поиска'
)
async def search_persons(
        query: str, page: int, size: int, person_service: PersonService = Depends(get_person_service)
) -> List[PersonDescription]:
    print('QUERY!', query, page)
    persons = await person_service.search_persons(query, page, size)
    if not persons:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='films with person not found')
    return persons


@router.get(
    '/{person_id}',
    response_model=PersonDescription,
    description='Получить информацию о персоне',
    response_description='Подробная информация о персоне'
)
async def person_details(
        person_id: str, person_service: PersonService = Depends(get_person_service)
) -> PersonDescription:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')
    return person


@router.get(
    '/{person_id}/film',
    response_model=List[FilmResponse],
    description='Получить фильмы по персоне.',
    response_description='Фильмы по персоне.'

)
async def list_film_by_person(
        person_id: str, person_service: PersonService = Depends(get_person_service)
) -> List[FilmResponse]:
    films = await person_service.get_film_by_id(person_id)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='films with person not found')
    return films
