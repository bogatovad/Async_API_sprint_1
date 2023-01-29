from elasticsearch import AsyncElasticsearch, helpers
import json
from pathlib import Path


class ElasticManager:
    def __init__(self, elastic_client: AsyncElasticsearch = None):
        self.test_data_path = Path(__file__).resolve().parent.parent / "testdata"
        self.elastic_client = elastic_client

    async def get_index_settings_from_file(self, file_name: str):
        with open(self.test_data_path / file_name, "r") as index_settings_file:
            index_settings = json.load(index_settings_file)
            return index_settings["settings"], index_settings["mappings"]

    async def get_data_from_file(self, file_name: str):
        with open(self.test_data_path / file_name, "r") as file_data:
            file_data = json.load(file_data)
            return file_data

    async def create_elastic_test_data(self):
        await self.create_indexes()
        await self.create_test_data()

    async def create_indexes(self):
        await self.create_index(index="movies", file_name="movies_index_settings.json")

    async def create_test_data(self):
        await self.create_test_data_from_file(file_name="films.json", index="movies")

    async def create_test_data_from_file(self, file_name: str, index: str):
        actions = await self.get_data_from_file(file_name)
        await helpers.async_bulk(client=self.elastic_client, actions=actions, index=index, refresh=True)

    async def create_index(self, file_name: str, index: str):
        settings, mappings = await self.get_index_settings_from_file(file_name)
        await self.elastic_client.indices.create(index=index, settings=settings, mappings=mappings, ignore=400)

    async def delete_elastic_test_data(self):
        await self.elastic_client.indices.delete(index="movies", ignore=[400, 404])
