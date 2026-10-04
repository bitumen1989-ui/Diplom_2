import allure
import pytest

from api_methods.api_user import User


@allure.epic("Тестирование сервиса Stellar Burgers")
@allure.feature("Создание пользователя")
class TestCreateUser:

    @allure.story("Успешное создание пользователя")
    @allure.title("Создание уникального пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_user_can_be_created(self, clear_user):
        response = User.create_user(clear_user)

        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "accessToken" in response.json()
        assert "refreshToken" in response.json()
        assert response.json()["user"]["email"] == clear_user["email"]
        assert response.json()["user"]["name"] == clear_user["name"]

    @allure.story("Ошибки при создании пользователя")
    @allure.title("Нельзя создать уже зарегистрированного пользователя")
    @allure.severity(allure.severity_level.NORMAL)
    def test_duplicate_user_cannot_be_created(self, clear_user):
        User.create_user(clear_user)
        response = User.create_user(clear_user)

        assert response.status_code == 403
        assert response.json()["success"] is False
        assert response.json()["message"] == "User already exists"

    @allure.story("Ошибки при создании пользователя")
    @allure.title("Нельзя создать пользователя без поля: {missing_field}")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_field(self, random_payload, missing_field):
        del random_payload[missing_field]
        response = User.create_user(random_payload)

        assert response.status_code == 403
        assert response.json()["success"] is False
        assert response.json()["message"] == "Email, password and name are required fields"