import pytest
import requests

HOST = 'http://docker.for.mac.localhost:8000'

@pytest.mark.parametrize(
    'endpoint', (
        'api/v1/genres/',
        'api/v1/genres/3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff',
        'api/v1/films/?page=1&size=10',
        'api/v1/films/3f8873be-f6b1-4f3f-8a01-873924659851',
        'api/v1/persons/search?query=Bieber&page=1&size=10',
        'api/v1/persons/a967bacf-35ca-42ef-9bfd-3d003a957125',
        'api/v1/persons/a967bacf-35ca-42ef-9bfd-3d003a957125/film'
    )
)
def test_endpoints_returns_status_code_200(endpoint):
    response = requests.get(f"{HOST}/{endpoint}")
    assert response.status_code == 200
