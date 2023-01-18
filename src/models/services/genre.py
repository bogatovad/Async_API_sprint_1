from models.mixins import IDMixin, ORJSONBaseModel


class Genre(IDMixin, ORJSONBaseModel):
    name: str


class GenreId(ORJSONBaseModel):
    id: str
    name: str
