from elasticsearch import AsyncElasticsearch

from services.data_storage import AsyncElasticDataStorage

es: AsyncElasticsearch | None


async def get_elastic() -> AsyncElasticsearch:
    """Функция для внедрения зависимостей."""
    return AsyncElasticDataStorage(es)
