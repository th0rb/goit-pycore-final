from collections import UserDict
from record import Record
from datetime import datetime, timedelta
from birthday import Birthday


class AddressBook(UserDict):

    def is_email_taken(self, email: str) -> bool:
        for _, rec in self.data.items():
            if any(e.value == email for e in getattr(rec, "emails", [])):
                return True
        return False

    def is_phone_taken(self, phone: str) -> bool:
        for _, rec in self.data.items():
            if any(p.value == phone for p in getattr(rec, "phones", [])):
                return True
        return False



    BIRTHDAY_REMINDER = 7

    def add_record(self, record: Record):
        if record.name.value in self.data:
            raise KeyError(f"Record with name '{record.name.value}' already exists.")
        self.data[record.name.value] = record

    def find(self, name: str):
        record = self.data.get(name, None)
        return record

    def delete(self, name: str):
        if name not in self.data:
            raise KeyError(f"Record with name '{name}' not found.")
        del self.data[name]

    def get_upcoming_birthdays(self):
        # Пошук записів, дні народження яких відбудуться протягом наступних days днів
        today = datetime.today().date()
        upcoming_birthdays = []
        for name, record in self.data.items():
            if record.birthday:
                birthday = record.birthday.value.replace(year=today.year).date()

                timedelta_days = (birthday - today).days

                if 0 <= timedelta_days <= self.BIRTHDAY_REMINDER:
                    #check for weekend
                    if birthday.weekday() > 4:
                        days_delta = 2 if birthday.weekday() == 5 else 1
                        congratulation_date = birthday + timedelta(days=days_delta)
                    else:
                        congratulation_date = birthday

                    upcoming_birthdays.append(
                        {
                            "name": name,
                            "congratulation_date": congratulation_date.strftime(
                                Birthday.DATE_FORMAT
                            ),
                        }
                    )

        return upcoming_birthdays
