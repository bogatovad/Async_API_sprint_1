from __future__ import annotations

from models.api.genre import Genre
from models.api.person import Person
from models.mixins import ORJSONBaseModel, UUIDMixin


class Film(UUIDMixin, ORJSONBaseModel):
    """Модель ответа API с информацией о фильмах."""
    title: str
    imdb_rating: float


class FilmDescription(Film):
    """Полная информация по фильму.
    Для ручки /api/v1/films/<uuid:UUID>/
    """
    description: str
    genre: list[Genre]
    actors: list[Person]
    writers: list[Person]
    directors: list[Person]
