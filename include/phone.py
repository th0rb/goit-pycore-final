import re
from field import Field


def normalize_phone(phone: str) -> str:
    """
    Нормалізує телефонний номер:
    - залишає тільки цифри та '+';
    - якщо номер починається з '+380' — ок;
    - якщо номер починається з '380' — додаємо '+';
    - якщо просто цифри — додаємо '+38';
    - повертає номер у міжнародному форматі.
    """
    cleaned = re.sub(r"[^\d+]", "", phone)

    if cleaned.startswith("+380"):
        return cleaned
    if cleaned.startswith("380"):
        return "+" + cleaned
    if cleaned.startswith("+"):
        return cleaned

    return "+38" + cleaned


class Phone(Field):
    def __init__(self, value: str):
        normalized = normalize_phone(value)

        # Дозволяємо тільки формат +380XXXXXXXXX  
        if not (normalized.startswith("+380") and len(normalized) == 13 and normalized[1:].isdigit()):
            raise ValueError("Phone number must be in format +380XXXXXXXXX.")

        super().__init__(normalized)

