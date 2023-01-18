from typing import List

from models.mixins import IDMixin, ORJSONBaseModel


class Person(IDMixin, ORJSONBaseModel):
    full_name: str


class PersonDescription(Person):
    """Данные по персоне.
    Для ручки /api/v1/persons/<uuid:UUID>/
    """
    role: str
    film_ids: List[str]
