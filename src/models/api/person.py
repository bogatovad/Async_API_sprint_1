from typing import List

from models.mixins import ORJSONBaseModel, UUIDMixin


class PersonResponse(UUIDMixin, ORJSONBaseModel):
    full_name: str


class PersonDescriptionResponse(PersonResponse):
    """Данные по персоне.
    Для ручки /api/v1/persons/<uuid:UUID>/
    """
    role: List[str]
    film_ids: List[str]
