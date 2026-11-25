"""Стартовые тесты клиента из предыдущего спринта."""

import os

import pytest
import requests
from models import CourierModel 
from dotenv import load_dotenv

from api_client import CourierAPIClient

load_dotenv()


@pytest.fixture(scope="session")
def client():
    """Создаёт клиент API для каждого теста."""
    base_url = os.getenv("API_BASE_URL", "http://127.0.0.1:5001/api")
    token = os.getenv("AUTH_TOKEN", "test_token_123")
    return CourierAPIClient(base_url, token)


@pytest.fixture
def new_courier_data():
    """Возвращает данные для создания курьера."""
    return {
        "first_name": "Мария",
        "last_name": "Сидорова",
        "phone": "+79997654321",
    }


@pytest.mark.usefixtures("fake_server")
class TestCourierClient:
    """Проверяет получение, создание и удаление курьера."""

    def test_get_courier_by_id(self, client):
        """Получает курьера, который уже есть на сервере."""
        courier = client.get_courier_by_id(1)
        assert courier["id"] == 1, "Убедитесь, что получен курьер с id=1."
        assert courier["first_name"] == "Иван", (
            "Убедитесь, что API вернул правильное имя курьера."
        )

    def test_create_courier(self, client, new_courier_data):
        result = client.create_courier(new_courier_data)
        validated = CourierModel(**result)  # валидация структуры

        assert "id" in result
        assert result["first_name"] == new_courier_data["first_name"]
        assert validated.id == result["id"]
        

    def test_update_courier(self, client):
        """Обновляет курьера и проверяет изменение имени."""
        new_courier_data = {"first_name": "Алексей", "last_name": "Петров", "type": "foot"}
        created = client.create_courier(new_courier_data)
        courier_id = created["id"]

        updated_data = {"first_name": "Дмитрий"}
        updated = client.update_courier(courier_id, updated_data)

        assert updated["first_name"] == "Дмитрий"

    def test_get_nonexistent_courier_raises(self, client):
        """Ожидает HTTPError при запросе несуществующего курьера."""
        with pytest.raises(requests.exceptions.HTTPError):
            client.get_courier_by_id(99999)

    def test_delete_and_verify_404_after_delete(self, client):
        new_courier_data = {"first_name": "Анна", "last_name": "Смирнова", "type": "foot"}
        created = client.create_courier(new_courier_data)
        courier_id = created["id"]

        client.delete_courier(courier_id)

        with pytest.raises(requests.exceptions.HTTPError):
            client.get_courier_by_id(courier_id) 

    def test_update_nonexistent_courier(self, client):
        nonexistent_id = 99999
        update_data = {"first_name": "НовыйИмя"}
        with pytest.raises(requests.exceptions.HTTPError):
            client.update_courier(nonexistent_id, update_data) 

    def test_create_courier_without_required_field_raises(self, client):
        invalid_data = {"last_name": "Сидорова", "phone": "+79997654321"}  # нет first_name
        with pytest.raises(requests.exceptions.HTTPError):
            client.create_courier(invalid_data)  