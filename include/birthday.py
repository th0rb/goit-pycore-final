from datetime import datetime
from field import Field


class Birthday(Field):

    DATE_FORMAT = "%d.%m.%Y"

    def __init__(self, value):
        try:
            dt = datetime.strptime(value, Birthday.DATE_FORMAT)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(dt)

    def __str__(self):
        return f'{self.value.strftime(Birthday.DATE_FORMAT)}'
    