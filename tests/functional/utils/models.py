from pydantic import BaseModel
from typing import Any


class HTTPResponse(BaseModel):
    body: Any
    status: int