from __future__ import annotations
from pydantic import BaseModel

from models.mixins import ORJSONBaseModel, UUIDMixin
from models.services.genre import Genre
from models.services.person import Person


class Film(UUIDMixin, ORJSONBaseModel):
    title: str
    imdb_rating: float
    description: str = ''
    genre: list[Genre] = []
    actors: list[Person] = []
    writers: list[Person] = []
    directors: list[Person] = []
