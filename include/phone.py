from field import Field


class Phone(Field):
    def __init__(self, value):
        # Перевірка на коректність формату (10 ціфр)
        if len(value) != 10 or not value.isdigit():
            raise ValueError("Phone number must be a string of 10 digits.")
        super().__init__(value)