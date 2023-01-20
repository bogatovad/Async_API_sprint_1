from typing import List, Optional

from pydantic import BaseModel, Field

from models.services.person import Person


class Film(BaseModel):
    id: str
    title: Optional[str]
    imdb_rating: Optional[float]
    description: Optional[str]
    genre: Optional[List[str]] = Field(default=[])
    actors: Optional[List[Person]] = Field(default=[])
    writers: Optional[List[Person]] = Field(default=[])
    director: Optional[List[str]] = Field(default=[])
