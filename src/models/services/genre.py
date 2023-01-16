from models.mixins import ORJSONBaseModel, UUIDMixin


class Genre(ORJSONBaseModel):
    name: str
