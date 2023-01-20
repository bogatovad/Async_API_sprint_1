from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request
from models.api.film import Film
from models.api.person import PersonFull
from services.person import PersonService, get_person_service

router = APIRouter()


@router.get(
    '/search',
    response_model=List[PersonFull],
    description='Поиск по персоне',
    response_description='Результат поиска'
)
async def search_persons(request: Request, person_service: PersonService = Depends(get_person_service))\
        -> List[PersonFull]:
    query_params = dict(request.query_params)
    persons = await person_service.search_persons(query_params)
    if not persons:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='films with person not found')
    return persons


@router.get(
    '/{person_id}',
    response_model=PersonFull,
    description='Получить информацию о персоне',
    response_description='Подробная информация о персоне'
)
async def person_details(person_id: str, person_service: PersonService = Depends(get_person_service)) -> PersonFull:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')
    return person


@router.get(
    '/{person_id}/film',
    response_model=List[Film],
    description='Получить фильмы по персоне.',
    response_description='Фильмы по персоне.'
)
async def list_film_by_person(
        person_id: str,
        person_service: PersonService = Depends(get_person_service)
) -> List[Film]:
    films = await person_service.get_film_by_id(person_id)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='films with person not found')
    return films
