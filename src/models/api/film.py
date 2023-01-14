from models.mixins import ORJSONBaseModel


class Film(ORJSONBaseModel):
    """Модель ответа API"""
    id: str
    title: str
