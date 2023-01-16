from __future__ import annotations

from models.mixins import ORJSONBaseModel, UUIDMixin


class Person(UUIDMixin, ORJSONBaseModel):
    full_name: str


class PersonDescription(Person):
    """Данные по персоне.
    Для ручки /api/v1/persons/<uuid:UUID>/
    """
    role: str
    film_ids: list[str]
