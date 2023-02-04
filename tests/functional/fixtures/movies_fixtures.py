import pytest
import uuid


@pytest.fixture
def generate_es_data():
    """Фикстура для генерации данных по фильмам."""
    data = [
        {
            'id': str(uuid.uuid4()),
            'imdb_rating': 8.5,
            'genre': ['Action', 'Sci-Fi'],
            'title': 'The Star',
            'description': 'New World',
            'director': ['Stan'],
            'actors_names': ['Ann', 'Bob'],
            'writers_names': ['Ben', 'Howard'],
            'actors': [
                {'id': '111', 'name': 'Ann'},
                {'id': '222', 'name': 'Bob'},
            ],
            'writers': [
                {'id': '333', 'name': 'Ben'},
                {'id': '444', 'name': 'Howard'}
            ],
        }
        for _ in range(60)
    ]
    data.append(
        {
            'id': str('12bb1b7e-b039-4f66-9248-b35d795e38f6'),
            'imdb_rating': 8.5,
            'genre': ['Action', 'Sci-Fi'],
            'title': 'The Star',
            'description': 'New World',
            'director': ['Stan'],
            'actors_names': ['Ann', 'Bob'],
            'writers_names': ['Ben', 'Howard'],
            'actors': [
                {'id': '111', 'name': 'Ann'},
                {'id': '222', 'name': 'Bob'},

            ],
            'writers': [
                {'id': '333', 'name': 'Ben'},
                {'id': '444', 'name': 'Howard'}
            ],
        }
    )
    return data


@pytest.fixture
def generate_expected_answer_for_all_films(generate_es_data):
    data = generate_es_data
    return [(item['id'], item['title'], item['imdb_rating']) for item in data]
