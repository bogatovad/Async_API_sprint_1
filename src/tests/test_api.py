from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_list_films():
    response = client.get("/api/v1/films/")
    assert response.status_code == 200


def test_list_genres():
    response = client.get('/api/v1/genres/')
    assert response.status_code == 200


def test_genre_details():
    response = client.get('/api/v1/genres/api/3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff')
    assert response.status_code == 200

