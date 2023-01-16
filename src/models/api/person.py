from __future__ import annotations

from models.mixins import ORJSONBaseModel, UUIDMixin


class Person(UUIDMixin, ORJSONBaseModel):
    full_name: str
