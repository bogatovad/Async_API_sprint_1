from src.models.mixins import ORJSONBaseModel, UUIDMixin


class Genre(UUIDMixin, ORJSONBaseModel):
    name: str
