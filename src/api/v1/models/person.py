from pydantic import Field

from core.mixins import ORJSONBaseModel, UUIDMixin


class PersonResponse(UUIDMixin, ORJSONBaseModel):
    name: str


class PersonDescriptionResponse(PersonResponse):
    """Данные по персоне.
    Для ручки /api/v1/persons/<uuid:UUID>/
    """
    role: list[str]
    film_ids: list[str]


class FilmPersonResponse(ORJSONBaseModel):
    uuid: str = Field(alias='id')
    name: str
