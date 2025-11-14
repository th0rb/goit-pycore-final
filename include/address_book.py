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
    
    #Повертає список контактів, у яких день народження відбудеться
    #протягом наступних BIRTHDAY_REMINDER днів.
    

        today = datetime.today().date()
        upcoming_birthdays = []

        for name, record in self.data.items():
            if record.birthday:

                birth_dt = record.birthday.value.date()
                birthday = birth_dt.replace(year=today.year)

                # Якщо в цьому році ДР вже минув — беремо наступний рік
                if birthday < today:
                    birthday = birthday.replace(year=today.year + 1)

                delta = (birthday - today).days

                if 0 <= delta <= self.BIRTHDAY_REMINDER:
                    upcoming_birthdays.append(
                        {
                            "name": name,
                            "birthday_date": birthday.strftime(Birthday.DATE_FORMAT),
                        }
                    )

        return upcoming_birthdays

