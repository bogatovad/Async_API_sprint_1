from models.services.person import Person
from pydantic import Field, BaseModel
from typing import List, Optional


class Film(BaseModel):
    id: str
    title: Optional[str]
    imdb_rating: Optional[float]
    description: Optional[str]
    genre: Optional[List[str]] = Field(default=[])
    actors: Optional[List[Person]] = Field(default=[])
    writers: Optional[List[Person]] = Field(default=[])
    director: Optional[List[str]] = Field(default=[])
