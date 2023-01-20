from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from models.api.film import FilmResponse
from models.api.person import PersonDescriptionResponse
from services.person import PersonService, get_person_service

router = APIRouter()


# todo: возможно тут стоит написать декоратор (или класс), который обобщает логику внутри этих функций.
@router.get(
    '/search',
    response_model=List[PersonDescriptionResponse],
    description='Поиск по персоне',
    response_description='Результат поиска'
)
async def search_persons(
        query: str,
        page: int = Query(1, description='Номер страницы'),
        size: int = Query(10, description='Количество персон на странице'),
        person_service: PersonService = Depends(get_person_service)
) -> List[PersonDescriptionResponse]:
    persons = await person_service.search_persons(query, page, size)
    if not persons:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='films with person not found')
    return [
        PersonDescriptionResponse(uuid=person.id, role=person.role, film_ids=person.film_ids, name=person.full_name)
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
