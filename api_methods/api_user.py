"""
Обёртки над эндпоинтами пользователя.
Каждый метод обёрнут в @allure.step — шаги видны в отчёте.
"""
import allure
import requests

from url import Url


class User:

    @staticmethod
    @allure.step("Создание пользователя с данными: {payload}")
    def create_user(payload: dict):
        return requests.post(Url.REGISTER, json=payload)

    @staticmethod
    @allure.step("Авторизация пользователя с данными: {payload}")
    def login_user(payload: dict):
        return requests.post(Url.LOGIN, json=payload)

    @staticmethod
    @allure.step("Удаление пользователя")
    def delete_user(token: str):
        return requests.delete(
            Url.USER, headers={"Authorization": token}
        )