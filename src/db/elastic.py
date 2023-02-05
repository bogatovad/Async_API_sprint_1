from elasticsearch import AsyncElasticsearch

es: AsyncElasticsearch | None


async def get_elastic() -> AsyncElasticsearch:
    """Функция для внедрения зависимостей."""
    return es
