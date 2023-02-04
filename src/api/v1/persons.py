from http import HTTPStatus
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from api.v1.models.film import FilmResponse
from api.v1.models.person import PersonDescriptionResponse
from core.messages import ErrorMessage
from services.person import PersonService, get_person_service

from fastapi import Request
from api.v1.common_paramaters import paginated_params

router = APIRouter()


@router.get(
    '/search',
    response_model=list[PersonDescriptionResponse],
    description='Поиск по персоне',
    response_description='Результат поиска'
)
async def search_persons(
        request: Request,
        common: dict = Depends(paginated_params),
        query: Optional[str] = Query('', description='Search string for query.'),
        person_service: PersonService = Depends(get_person_service)
) -> List[PersonDescriptionResponse]:
    query_params = dict(
        **common,
        query=query,
        request=request,
    )
    persons = await person_service.search_persons(query_params)
    if not persons:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=ErrorMessage.PERSON_NOT_FOUND)
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
        request: Request,
        person_id: str,
        person_service: PersonService = Depends(get_person_service)
) -> PersonDescriptionResponse:
    query_params = dict(
        person_id=person_id,
        request=request
    )
    person = await person_service.get_by_id(query_params)
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
