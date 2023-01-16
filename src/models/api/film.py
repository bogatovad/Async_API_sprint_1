from __future__ import annotations
from models.mixins import ORJSONBaseModel, UUIDMixin


class Film(UUIDMixin, ORJSONBaseModel):
    """Модель ответа API с информацией о фильмах."""
    title: str