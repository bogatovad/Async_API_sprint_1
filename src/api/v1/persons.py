from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from models.api.film import Film
from models.api.person import PersonFull
from models.services.genre import GenreId
from services.film import PersonService, get_person_service
from typing import List

router = APIRouter()


@router.get('/search', response_model=List[PersonFull])
async def search_persons(query: str, page: int, size: int, person_service: PersonService = Depends(get_person_service)) -> \
        List[PersonFull]:
    print('QUERY!', query, page)
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


