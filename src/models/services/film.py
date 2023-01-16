from models.mixins import ORJSONBaseModel


class Film(ORJSONBaseModel):
    id: str
    title: str
    description: str
