from models.mixins import IDMixin, ORJSONBaseModel


class Person(IDMixin, ORJSONBaseModel):
    full_name: str
