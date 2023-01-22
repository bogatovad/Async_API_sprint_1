from core.mixins import ORJSONBaseModel, UUIDMixin


class GenreResponse(UUIDMixin, ORJSONBaseModel):
    name: str
