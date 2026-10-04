"""
Генераторы тестовых данных для API-тестов Stellar Burgers.
"""
import random

from faker import Faker


faker = Faker("ru_RU")


def generate_user_data() -> dict:
    """Генерирует данные нового пользователя."""
    name = faker.first_name()
    digits = f"{random.randint(0, 9999):04d}"
    email = f"sergey_kuznetsov_45_{digits}@yandex.ru"
    password = faker.password(length=6, special_chars=True, digits=True)

    return {
        "email": email,
        "password": password,
        "name": name,
    }


def generate_invalid_hash() -> str:
    """
    Генерирует невалидный хэш ингредиента.
    Возвращает чистую строку — без лишних кавычек.
    """
    return "".join(random.choices("abcdef0123456789", k=24))