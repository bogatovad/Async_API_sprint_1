from models.mixins import ORJSONBaseModel, UUIDMixin


class GenreResponse(UUIDMixin, ORJSONBaseModel):
    name: str
