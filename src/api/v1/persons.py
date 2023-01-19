from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from models.api.film import Film
from models.api.person import PersonFull
from services.person import PersonService, get_person_service
from typing import List

router = APIRouter()


# todo: возможно тут стоит написать декоратор (или класс), который обобщает логику внутри этих функций.

@router.get('/search', response_model=List[PersonFull])
async def search_persons(query: str, page: int, size: int, person_service: PersonService = Depends(get_person_service))\
        -> List[PersonFull]:
    persons = await person_service.search_persons(query, page, size)
    if not persons:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='films with person not found')
    return persons


@router.get('/{person_id}', response_model=PersonFull)
async def person_details(person_id: str, person_service: PersonService = Depends(get_person_service)) -> PersonFull:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')
    return person


@router.get('/{person_id}/film', response_model=List[Film])
async def list_film_by_person(person_id: str, person_service: PersonService = Depends(get_person_service)) -> List[Film]:
    films = await person_service.get_film_by_id(person_id)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='films with person not found')
    return films


