from api.v1.models.person import FilmPersonResponse
from core.mixins import ORJSONBaseModel, UUIDMixin
from typing import Optional


class FilmResponse(UUIDMixin, ORJSONBaseModel):
    """Модель ответа API с информацией о фильмах."""
    title: str
    imdb_rating: Optional[float]


class FilmDescriptionResponse(FilmResponse):
    """Полная информация по фильму.
    Для ручки /api/v1/films/<uuid:UUID>/
    """
    description: str | None
    genre: list[str] | None
    actors: list[FilmPersonResponse] | None
    writers: list[FilmPersonResponse] | None
    directors: list[str] | None
