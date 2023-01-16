from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from pydantic import BaseModel


FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут


class BaseService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch, index: str, model):
        self.redis = redis
        self.elastic = elastic
        self.index = index
        self.model = model

    async def get_by_id(self, id: str):
        item = await self._get_from_cache(id)
        if not item:
            item = await self._get_from_elastic(id)
            if not item:
                return None
            await self._put_to_cache(item)

        return item

    async def get_list(self):
        try:
            docs = await self.elastic.search(
                index=self.index,
                body={"query": {"match_all": {}}},
                size=50
            )
            items = docs['hits']['hits']
            schema = [self.model(**doc['_source']) for doc in items]
        except NotFoundError:
            return None
        return schema

    async def _get_from_elastic(self, id: str):
        try:
            doc = await self.elastic.get(self.index, id)
        except NotFoundError:
            return None
        return self.model(**doc['_source'])

    async def _get_from_cache(self, id: str):
        data = await self.redis.get(id)
        if not data:
            return None

        item = self.model.parse_raw(data)
        return item

    async def _put_to_cache(self, model):
        await self.redis.set(model.id, model.json(), expire=FILM_CACHE_EXPIRE_IN_SECONDS)

