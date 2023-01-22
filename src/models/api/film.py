from typing import List, Optional

from core.mixins import ORJSONBaseModel, UUIDMixin
from models.api.person import FilmPersonResponse


class FilmResponse(UUIDMixin, ORJSONBaseModel):
    """Модель ответа API с информацией о фильмах."""
    title: str
    imdb_rating: float


class FilmDescriptionResponse(FilmResponse):
    """Полная информация по фильму.
    Для ручки /api/v1/films/<uuid:UUID>/
    """
    description: Optional[str]
    genre: Optional[List[str]]
    actors: Optional[List[FilmPersonResponse]]
    writers: Optional[List[FilmPersonResponse]]
    directors: Optional[List[str]]
