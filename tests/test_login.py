import allure
import pytest

from api_methods.api_user import User


@allure.epic("Тестирование сервиса Stellar Burgers")
@allure.feature("Авторизация пользователя")
class TestLoginUser:

    @allure.story("Успешная авторизация")
    @allure.title("Вход под существующим пользователем")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_existing_user_can_login(self, create_delete_user):
        response = User.login_user(create_delete_user)

        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "accessToken" in response.json()
        assert "refreshToken" in response.json()
        assert response.json()["user"]["email"] == create_delete_user["email"]

    @allure.story("Ошибка авторизации")
    @allure.title("Вход с неверным полем: {field}")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("field, value", [
        ["email", "wrong@yandex.ru"],
        ["password", "wrong_password"],
    ])
    def test_login_with_invalid_credentials(self, create_delete_user, field, value):
        payload = dict(create_delete_user)
        payload[field] = value

        response = User.login_user(payload)

        assert response.status_code == 401
        assert response.json()["success"] is False
        assert response.json()["message"] == "email or password are incorrect"