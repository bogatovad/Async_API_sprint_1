from models.mixins import ORJSONBaseModel


class Person(ORJSONBaseModel):
    id: str
    name: str
