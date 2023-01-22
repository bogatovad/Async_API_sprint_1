from core.mixins import IDMixin, ORJSONBaseModel


class Genre(IDMixin, ORJSONBaseModel):
    id: str
    name: str
