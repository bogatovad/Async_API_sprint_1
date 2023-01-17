from typing import List

from models.mixins import ORJSONBaseModel, UUIDMixin
from models.services.person import Person
from pydantic import Field
from typing import List, Optional

class Film(UUIDMixin, ORJSONBaseModel):
    title: Optional[str]
    imdb_rating: Optional[float]
    description: Optional[str]
    genre: Optional[List[str]] = Field(default=[])
    actors: Optional[List[Person]] = Field(default=[])
    writers: Optional[List[Person]] = Field(default=[])
    director: Optional[List[str]] = Field(default=[])
