import re
from field import Field


def normalize_phone(phone: str) -> str:
    """
    Нормалізує телефонний номер:
    - дозволяє тільки цифри, '+', '-', '(', ')', пробіли;
    - якщо є інші символи → помилка;
    - формує номер у форматі +380XXXXXXXXX.
    """
    # Дозволені символи: цифри, +, -, пробіли, круглі дужки
    if re.search(r"[^\d+\-\s()]", phone):
        raise ValueError("Phone number contains invalid characters (letters or symbols).")

    # Прибираємо пробіли, дужки, тире
    cleaned = re.sub(r"[()\s\-]", "", phone)

    # Тепер у cleaned можуть бути тільки цифри або +цифри
    # Виправляємо різні варіанти форматів
    if cleaned.startswith("+380"):
        number = cleaned
    elif cleaned.startswith("380"):
        number = "+" + cleaned
    elif cleaned.startswith("0") and len(cleaned) == 10:
        number = "+38" + cleaned
    elif cleaned.startswith("+") and not cleaned.startswith("+380"):
        raise ValueError("Only Ukrainian numbers in +380 format are allowed.")
    else:
        raise ValueError("Invalid phone number format. Phone number must be in format +380XXXXXXXXX.")

    # Фінальна перевірка
    if not (number.startswith("+380") and len(number) == 13 and number[1:].isdigit()):
        raise ValueError("Phone number must be in format +380XXXXXXXXX.")

    return number



class Phone(Field):
    def __init__(self, value: str):
        normalized = normalize_phone(value)
        super().__init__(normalized)

