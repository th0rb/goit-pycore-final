import re
from field import Field

class Email(Field):
    # Розширений, реалістичний, production-рівня regex (близький до RFC 5322)
    EMAIL_REGEX = re.compile(
        r"^(?=.{6,254}$)"                                      # Довжина email
        r"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+"                    # local-part
        r"@"
        r"(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+"# домени
        r"[A-Za-z]{2,}$"                                       # TLD
    )

    def __init__(self, value: str):
        normalized = value.strip().lower()

        if not self.EMAIL_REGEX.match(normalized):
            raise ValueError("Невірний формат email.")

        super().__init__(normalized)
