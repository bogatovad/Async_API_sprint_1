def es_search_template(index, query_params: dict) -> dict:
    """Шаблон для построения поисковых запросов к elasticsearch."""
    page_size_default = 50
    number_page_default = 1

    query_fields_movies = [
        'title',
        'description',
        'genre',
        'actors_names'
    ]
    query_fields_persons = [
        'full_name'
    ]

    # возможные поля для фильтрации.
    query_fields = {
        "movies": query_fields_movies,
        "persons": query_fields_persons
    }

    # поле по умолчанию, если пришел запрос с ?query=...
    field_for_query = {
        "movies": "title",
        "persons": "full_name"
    }

    # поле по умолчанию для сортировки.
    field_for_sort = {
        "movies": "imdb_rating",
        "persons": "id"
    }

    # получаем данные для сортировки: sort, направление сортировки ( desc, asc ).
    query_sort = query_params.get('sort')
    query_order_sort = 'desc' if query_sort and query_sort[0] == '-' else 'asc'
    query_field_sort = query_sort if query_sort is not None else field_for_sort[index]
    query_field_sort = query_field_sort[1:] if query_sort and query_sort[0] == '-' else query_field_sort

    # получаем данные для установки размера страницы: page[size].
    query_size = query_params.get('page[size]')
    query_size_data = query_size if query_size is not None else page_size_default

    # получаем поле по которому происходит фильтрация.
    # формат поля: filter[genre], filter[title], ...
    value_filter_field = ''
    filter_field = ''

    for field in query_fields[index]:
        _filter_field = f'filter[{field}]'
        _value_filter_field = query_params.get(_filter_field)
        if _value_filter_field is not None:
            filter_field = field
            value_filter_field = _value_filter_field

    # получаем поле ?query=...
    query = query_params.get('query')
    if query is not None:
        filter_field = field_for_query[index]
        value_filter_field = query

    query_template = {
        "query": {
            "match": {
                f"{filter_field}": f"{value_filter_field}"
            }
        },
        "sort": {f"{query_field_sort}": f"{query_order_sort}"},
        "size": query_size_data
    }

    query_number_page = query_params.get('page[number]')
    number_page = query_number_page if query_number_page is not None else number_page_default
    return number_page, query_template
