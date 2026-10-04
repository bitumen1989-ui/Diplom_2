"""
Обёртки над эндпоинтами заказов и ингредиентов.
"""
import allure
import requests

from url import Url


class Order:

    @staticmethod
    @allure.step("Получение данных об ингредиентах")
    def get_ingredients():
        return requests.get(Url.INGREDIENTS)

    @staticmethod
    @allure.step("Создание заказа с payload: {payload}")
    def create_order(payload: dict, token: str = None):
        headers = {"Authorization": token} if token else {}
        return requests.post(Url.ORDERS, headers=headers, json=payload)