from __future__ import annotations

from typing import List

from models.mixins import ORJSONBaseModel, UUIDMixin


class Person(UUIDMixin, ORJSONBaseModel):
    full_name: str


class PersonFull(UUIDMixin, ORJSONBaseModel):
    full_name: str
    role: List[str]
    film_ids: List[str]
