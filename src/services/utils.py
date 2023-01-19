
def es_search_template(query_params: dict) -> dict:

    page_sz = 20
    page_num = 0
    sort = 'imdb_rating'
    order = 'desc'
    filter_id = None
    filter_path = None
    query = None
    query_fields = ['title,', 'description']


    if query_params.get('sort'):
        if not query_params.get('sort')[0] == '-':
            order = 'asc'

    if query_params.get('filter[genre]'):
        filter_id = query_params.get('filter[genre]')
        filter_path = 'genre'
    if query_params.get('filter[person]'):
        filter_id = query_params.get('filter[person]')
    if query_params.get('filter[path]'):
        filter_path = query_params.get('filter[path]')
    if query_params.get('query'):
        query = query_params.get('query')
    if query_params.get('fields'):
        query_fields = [query_params.get('fields')]

    search_query = {'query_string': {'fields': query_fields, 'query': f'{query}~'}}
    filter = {
        'nested': {
            'path': filter_path,
            'query': {'bool': {'must': [{'match_phrase': {f'{filter_path}.uuid': filter_id}}]}},
        }
    }

    search_template = dict()
    search_sort = [{sort: {'order': order}}]
    if sort:
        search_template['sort'] = search_sort
    if filter_id:
        search_template['query'] = filter
    if query:
        search_template['query'] = search_query

    return search_template
