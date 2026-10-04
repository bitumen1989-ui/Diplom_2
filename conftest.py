"""
Фикстуры для тестов API Stellar Burgers.
"""
import pytest

from api_methods.api_order import Order
from api_methods.api_user import User
from data_generator import generate_user_data


@pytest.fixture(scope="function")
def random_payload() -> dict:
    """Генерирует случайные данные пользователя (без создания)."""
    return generate_user_data()


@pytest.fixture(scope="function")
def clear_user(random_payload: dict):
    """
    Отдаёт данные пользователя в тест и удаляет его после.
    Если пользователь не был создан — cleanup просто ничего не сделает.
    """
    yield random_payload

    login_response = User.login_user(random_payload)
    if login_response.status_code == 200:
        token = login_response.json()["accessToken"]
        User.delete_user(token)


@pytest.fixture(scope="function")
def create_delete_user(random_payload: dict):
    """
    Создаёт пользователя до теста и удаляет после.
    Используется, когда тесту нужен уже существующий пользователь.
    """
    User.create_user(random_payload)

    yield random_payload

    login_response = User.login_user(random_payload)
    if login_response.status_code == 200:
        token = login_response.json()["accessToken"]
        User.delete_user(token)


@pytest.fixture(scope="function")
def ingredient_ids() -> list:
    """
    Получает актуальные ID ингредиентов с сервера.
    Не хардкодим — они могут измениться.
    """
    response = Order.get_ingredients()
    ingredients = response.json()["data"]
    return [item["_id"] for item in ingredients[:2]]