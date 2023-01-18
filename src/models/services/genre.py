from models.mixins import ORJSONBaseModel


class Genre(ORJSONBaseModel):
    name: str


class GenreId(ORJSONBaseModel):
    id: str
    name: str
