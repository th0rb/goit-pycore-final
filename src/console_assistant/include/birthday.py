from datetime import datetime
from field import Field


class Birthday(Field):

    DATE_FORMAT = "%d.%m.%Y"

    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, Birthday.DATE_FORMAT)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self):
        return f'{self.value.strftime(Birthday.DATE_FORMAT)}'    