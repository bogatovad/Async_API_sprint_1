from typing import List

from pydantic import Field

from core.mixins import ORJSONBaseModel, UUIDMixin


class PersonResponse(UUIDMixin, ORJSONBaseModel):
    name: str


class PersonDescriptionResponse(PersonResponse):
    """Данные по персоне.
    Для ручки /api/v1/persons/<uuid:UUID>/
    """
    role: List[str]
    film_ids: List[str]


class FilmPersonResponse(ORJSONBaseModel):
    uuid: str = Field(alias='id')
    name: str
