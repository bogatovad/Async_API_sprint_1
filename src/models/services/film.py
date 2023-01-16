from typing import List

from models.mixins import ORJSONBaseModel, UUIDMixin
from models.services.genre import Genre
from models.services.person import Person


class Film(UUIDMixin, ORJSONBaseModel):
    title: str
    imdb_rating: float
    description: str = ''
    genre: List[Genre] = []
    actors: List[Person] = []
    writers: List[Person] = []
    directors: List[Person] = []
