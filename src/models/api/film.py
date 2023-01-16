from models.mixins import ORJSONBaseModel, UUIDMixin


class Film(UUIDMixin, ORJSONBaseModel):
    """Модель ответа API с информацией о фильмах."""
    title: str
    imdb_rating: float