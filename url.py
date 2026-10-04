"""
Адреса эндпоинтов API Stellar Burgers.
Только те, что используются в тестах — без лишнего.
"""


class Url:
    BASE_URL = "https://stellarburgers.education-services.ru"

    REGISTER = f"{BASE_URL}/api/auth/register"
    LOGIN = f"{BASE_URL}/api/auth/login"
    USER = f"{BASE_URL}/api/auth/user"

    INGREDIENTS = f"{BASE_URL}/api/ingredients"
    ORDERS = f"{BASE_URL}/api/orders"