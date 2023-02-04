from fastapi import Query


async def paginated_params(
        page_size: int | None = Query(10, alias='page[size]'),
        page_number: int | None = Query(1, alias='page[number]')
):
    """Функция-провайдер, возвращаем параметры пагинации."""
    return {"page_size": page_size, "page_number": page_number}
