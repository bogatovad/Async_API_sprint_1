import http

import pytest

@pytest.mark.asyncio
async def test_get_nonexistent_film(make_get_request):
    response = await make_get_request(method="/film/a")
    assert response.status == http.HTTPStatus.NOT_FOUND
