
from typing import Optional
from elasticsearch import AsyncElasticsearch

es: AsyncElasticsearch | None = None


async def get_elastic() -> AsyncElasticsearch:
    """Функция для внедрения зависимостей."""
    return es
