from src.models.mixins import ORJSONBaseModel, UUIDMixin


class Person(UUIDMixin, ORJSONBaseModel):
    full_name: str
