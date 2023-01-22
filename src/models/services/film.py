from pydantic import Field

from models.mixins import IDMixin, ORJSONBaseModel
from models.services.person import FilmPerson


class FilmShort(IDMixin, ORJSONBaseModel):
    title: str
    imdb_rating: float


class Film(FilmShort):
    title: str | None
    imdb_rating: float | None
    description: str | None
    genre: list[str] | None = Field(default=[])
    actors: list[FilmPerson] | None = Field(default=[])
    writers: list[FilmPerson] | None = Field(default=[])
    director: list[str] | None = Field(default=[])
