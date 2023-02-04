import pytest
import uuid


@pytest.fixture
def generate_es_data_person():
    """Фикстура для генерации данных по персонажам."""
    persons = [
        {
            'id': str(uuid.uuid4()),
            'full_name': 'Petr Ivanov',
        }
        for _ in range(60)
    ]
    persons.extend([
        {'id': '42b40c6b-4d07-442f-b652-4ec1ee8b57gg', 'full_name': 'Ivan Petrov'}
    ])
    return persons
