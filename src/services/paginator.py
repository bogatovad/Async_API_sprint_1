class Paginator:
    async def paginator(self, index: str, query_params: dict, page: int):
        doc = await self.elastic.search(
            index=index,
            body=query_params
        )

        data = doc['hits']['hits']

        if not data:
            return []

        last_item = data[-1]
        search_after = last_item['sort']
        query_params['search_after'] = search_after

        for item_page in range(1, page):
            docs = await self.elastic.search(index=index, body=query_params)
            data = docs['hits']['hits']
            if not data:
                break
            last_item = data[-1]
            search_after = last_item['sort']
            query_params['search_after'] = search_after

        return data
