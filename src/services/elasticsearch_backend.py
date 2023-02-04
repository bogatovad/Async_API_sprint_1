from abc import ABC
from elasticsearch import AsyncElasticsearch, NotFoundError


class SearchBackend(ABC):
    """Интерфейс для класса, реализующего методы поиска и вывода данных."""

    async def get_by_id(self, id):
        """Получение объекта по id из хранилища."""
        pass

    async def get_list(self, data):
        """Получение списка объектов из хранилища."""
        pass

    async def search(self, key):
        """Поиск объектов в хранилище."""
        pass



class ElasticService(SearchBackend):
    """Класс, реализующий методы поиска и вывода данных в Elasticsearch."""

    def __init__(self, elastic: AsyncElasticsearch):
        self.elastic = elastic

    async def get_by_id(self, index, id):
        try:
            doc = await self.elastic.get(index, id)
        except NotFoundError:
            return None
        return doc['_source']
