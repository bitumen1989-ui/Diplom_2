import allure

from api_methods.api_order import Order
from api_methods.api_user import User
from data_generator import generate_invalid_hash


@allure.epic("Тестирование сервиса Stellar Burgers")
@allure.feature("Создание заказа")
class TestCreateOrder:

    # ---------- Успешное создание ----------

    @allure.story("Успешное создание заказа")
    @allure.title("Создание заказа с авторизацией и с ингредиентами")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_order_can_be_created_with_authorization(
        self, create_delete_user, ingredient_ids
    ):
        login_response = User.login_user(create_delete_user)
        token = login_response.json()["accessToken"]

        payload = {"ingredients": ingredient_ids}
        response = Order.create_order(payload, token)

        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "name" in response.json()
        assert "order" in response.json()
        assert isinstance(response.json()["order"]["number"], int)
        assert response.json()["order"]["number"] > 0

    @allure.story("Успешное создание заказа")
    @allure.title("Создание заказа без авторизации")
    @allure.severity(allure.severity_level.NORMAL)
    def test_unauthorized_user_create_order(self, ingredient_ids):
        payload = {"ingredients": ingredient_ids}
        response = Order.create_order(payload)

        # Фактическое поведение сервиса: заказ создаётся и без токена (200).
        # Документация обещает 401 — расхождение задокументировано в README.
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "order" in response.json()

    # ---------- Создание без ингредиентов ----------

    @allure.story("Ошибки при создании заказа")
    @allure.title("Нельзя создать заказ без ингредиентов (с авторизацией)")
    @allure.severity(allure.severity_level.NORMAL)
    def test_order_without_ingredients_with_auth(self, create_delete_user):
        login_response = User.login_user(create_delete_user)
        token = login_response.json()["accessToken"]

        response = Order.create_order({"ingredients": []}, token)

        assert response.status_code == 400
        assert response.json()["success"] is False
        assert response.json()["message"] == "Ingredient ids must be provided"

    # ---------- Невалидный хэш ----------

    @allure.story("Ошибки при создании заказа")
    @allure.title("Нельзя создать заказ с неверным хешем ингредиентов")
    @allure.severity(allure.severity_level.NORMAL)
    def test_order_with_invalid_hash_returns_error(self, create_delete_user):
        login_response = User.login_user(create_delete_user)
        token = login_response.json()["accessToken"]

        payload = {"ingredients": [generate_invalid_hash()]}
        response = Order.create_order(payload, token)

        # Фактическое поведение сервиса: 400 Bad Request.
        # Документация обещает 500 — расхождение задокументировано в README.
        assert response.status_code == 400