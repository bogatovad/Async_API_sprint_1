from typing import List

from models.api.genre import GenreResponse
from models.api.person import Person
from models.mixins import ORJSONBaseModel, UUIDMixin


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
    actors: List[Person]
    writers: List[Person]
    directors: List[Person]
