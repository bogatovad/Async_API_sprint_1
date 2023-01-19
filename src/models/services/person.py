from typing import List

from models.mixins import IDMixin, ORJSONBaseModel, UUIDMixin


class Person(IDMixin, ORJSONBaseModel):
    full_name: str


class PersonDescription(Person):
    """Данные по персоне.
    Для ручки /api/v1/persons/<uuid:UUID>/
    """
    role: List[str]
    film_ids: List[str]


class PersonFull(IDMixin, ORJSONBaseModel):
    full_name: str
    role: List[str]
    film_ids: List[str]
