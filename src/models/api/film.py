from typing import List, Optional
from models.mixins import ORJSONBaseModel, UUIDMixin

from .genre import Genre
from .person import Person


class Film(UUIDMixin, ORJSONBaseModel):
    """Модель ответа API с информацией о фильмах."""
    title: str
    imdb_rating: Optional[float]


class FilmDescription(Film):
    """Полная информация по фильму.
    Для ручки /api/v1/films/<uuid:UUID>/
    """
    description: Optional[str]
