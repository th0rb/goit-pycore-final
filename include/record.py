from name import Name
from phone import Phone
from birthday import Birthday
from email_field import Email


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.emails: list[Email] = [] 
        self.birthday = None

    def add_phone(self, phone_number):
        self.phones.append(Phone(phone_number))

    def remove_phone(self, phone_number):
        self.phones = list(filter(lambda p: p.value != phone_number, self.phones))
    
    def edit_phone(self, old_phone, new_phone):
        self.phones = list(map(lambda phone: Phone(new_phone) if phone.value == old_phone else phone, self.phones))

    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None
    
    def add_email(self, value: str) -> None:
        self.emails.append(Email(value))

    def find_email(self, value: str) -> Email | None:
        return next((e for e in self.emails if e.value == value), None)

    def remove_email(self, value: str) -> None:
        e = self.find_email(value)
        if not e:
            raise KeyError("Email not found")
        self.emails.remove(e)

    def edit_email(self, old_value: str, new_value: str) -> None:
        e = self.find_email(old_value)
        if not e:
            raise KeyError("Email not found")
        idx = self.emails.index(e)
        self.emails[idx] = Email(new_value)
    
    def add_birthday(self, birthday):
        if not self.birthday:
            self.birthday = Birthday(birthday)
        else:
            raise ValueError("Birthday already exists for this record.")

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
