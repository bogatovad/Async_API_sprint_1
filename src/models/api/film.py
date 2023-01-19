from models.mixins import ORJSONBaseModel, UUIDMixin
from typing import List

from models.api.genre import GenreResponse
from models.api.person import PersonResponse


class FilmResponse(UUIDMixin, ORJSONBaseModel):
    """Модель ответа API с информацией о фильмах."""
    title: str
    imdb_rating: float


class FilmDescriptionResponse(FilmResponse):
    """Полная информация по фильму.
    Для ручки /api/v1/films/<uuid:UUID>/
    """
    description: str
    genre: List[GenreResponse]
    actors: List[PersonResponse]
    writers: List[PersonResponse]
    directors: List[PersonResponse]
