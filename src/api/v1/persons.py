from http import HTTPStatus
from typing import List, Optional

from fastapi import Query

from fastapi import APIRouter, Depends, HTTPException
from api.v1.models.film import FilmResponse
from api.v1.models.person import PersonDescriptionResponse

from core.messages import ErrorMessage
from services.person import PersonService, get_person_service

router = APIRouter()


@router.get(
    '/search',
    response_model=list[PersonDescriptionResponse],
    description='Поиск по персоне',
    response_description='Результат поиска'
)
async def search_persons(
        page_size: Optional[int] = Query(1, alias='page[size]', description='Items amount on page', ge=1),
        page_number: Optional[int] = Query(10, alias='page[number]', description='Page number for pagination', ge=1),
        query: Optional[str] = Query('', description='Search string for query.'),
        person_service: PersonService = Depends(get_person_service)
) -> List[PersonDescriptionResponse]:
    query_params = dict(
        page_size=page_size,
        page_number=page_number,
        query=query,
    )
    persons = await person_service.search_persons(query_params)
    if not persons:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=ErrorMessage.PERSON_FILMWORK_NOT_FOUND)
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
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=ErrorMessage.PERSON_NOT_FOUND)
    return PersonDescriptionResponse(uuid=person.id, role=person.role, film_ids=person.film_ids, name=person.full_name)


@router.get(
    '/{person_id}/film',
    response_model=list[FilmResponse],
    description='Получить фильмы по персоне.',
    response_description='Фильмы по персоне.'

)
async def list_film_by_person(
        person_id: str,
        person_service: PersonService = Depends(get_person_service)
) -> list[FilmResponse]:
    films = await person_service.get_film_by_id(person_id)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=ErrorMessage.PERSON_FILMWORK_NOT_FOUND)
    return [FilmResponse(uuid=film.id, title=film.title, imdb_rating=film.imdb_rating) for film in films]
