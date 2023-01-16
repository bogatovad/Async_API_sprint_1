from pydantic import BaseModel, Field


class Genre(BaseModel):
    id: str
    name: str
