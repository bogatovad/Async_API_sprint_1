from elasticsearch import AsyncElasticsearch

from services.data_storage import AsyncElasticDataStorage

es: AsyncElasticDataStorage | None


async def get_elastic() -> AsyncElasticDataStorage:
    """Функция для внедрения зависимостей."""
    return es
