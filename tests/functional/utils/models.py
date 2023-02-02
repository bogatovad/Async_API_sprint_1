from pydantic import BaseModel
from typing import Any


class HTTPResponse(BaseModel):
    body: Any
    status: int


class Genre(BaseModel):
    id: str
    name: str