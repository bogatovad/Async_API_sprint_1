from typing import List, Optional

from pydantic import Field

from models.mixins import IDMixin, ORJSONBaseModel
from models.services.person import Person


class FilmShort(IDMixin, ORJSONBaseModel):
    title: str
    imdb_rating: float


class Film(FilmShort):
    title: Optional[str]
    imdb_rating: Optional[float]
    description: Optional[str]
    genre: Optional[List[str]] = Field(default=[])
    actors: Optional[List[Person]] = Field(default=[])
    writers: Optional[List[Person]] = Field(default=[])
    director: Optional[List[str]] = Field(default=[])
