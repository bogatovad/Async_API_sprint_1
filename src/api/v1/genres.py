from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from models.services.genre import GenreId
from services.film import GenreService, get_genre_service
from typing import List

router = APIRouter()


@router.get('/', response_model=List[GenreId])
async def list_genres(genre_service: GenreService = Depends(get_genre_service)) -> List[GenreId]:
    genres = await genre_service.get_list()
    if not genres:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='genres not found')
    return genres
