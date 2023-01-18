from models.mixins import IDMixin, ORJSONBaseModel


class Genre(IDMixin, ORJSONBaseModel):
    name: str
