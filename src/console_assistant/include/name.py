from field import Field


class Name(Field):
    def __init__(self, value):
        #обов'язкове поле
        if len(value.strip()) == 0:
            raise ValueError("Name cannot be empty.")
        super().__init__(value)
