import pytest
import uuid


@pytest.fixture
def generate_es_data_genre():
    """Фикстура для генерации данных по жанрам."""
    genres = [
            {
                'id': str(uuid.uuid4()),
                'name': 'Thriller',
                'description': 'Thrilling and scary'
            }
            for _ in range(9)
        ]
    genres.append(
        {
            'id': '9c91a5b2-eb70-4889-8581-ebe427370edd',
            'name': 'Musical',
            'description': 'Nice and dancy'
        }
    )
    return genres
