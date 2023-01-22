from models.mixins import IDMixin, ORJSONBaseModel


class Person(IDMixin, ORJSONBaseModel):
    full_name: str


class FilmPerson(IDMixin, ORJSONBaseModel):
    name: str


class PersonDescription(Person):
    """Данные по персоне.
    Для ручки /api/v1/persons/<uuid:UUID>/
    """
    role: list[str]
    film_ids: list[str]
