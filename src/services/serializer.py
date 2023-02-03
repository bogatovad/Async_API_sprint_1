import pickle
from abc import ABC


class SerializeData(ABC):
    def serialize(self, data):
        """Сериализация данных."""
        pass

    def deserialize(self, data):
        """Распаковка данных."""
        pass


class PickleSerializeData(SerializeData):
    def serialize(self, data):
        return pickle.dumps(data)

    def deserialize(self, data):
        return pickle.loads(data)
