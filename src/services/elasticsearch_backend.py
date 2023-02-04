from abc import ABC
from elasticsearch import AsyncElasticsearch, NotFoundError


class DataStorageBackend(ABC):
    """Интерфейс, реализующего методы работы с хранилищем данных."""

    async def get_data_by_id(self, id):
        """Получение объекта по id из хранилища."""
        pass

    async def get_data_list(self, data):
        """Получение списка объектов из хранилища."""
        pass

    async def search(self, key):
        """Поиск объектов в хранилище."""
        pass



class ElasticService(DataStorageBackend):
    """Класс, реализующий методы работы с Elasticsearch."""

    def __init__(self, elastic: AsyncElasticsearch):
        self.elastic = elastic

    async def get_data_by_id(self, id):
        try:
            doc = await self.elastic.get(id)
        except NotFoundError:
            return None
        return doc