from name import Name
from phone import Phone
from birthday import Birthday


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
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
    
    def add_birthday(self, birthday):
        if not self.birthday:
            self.birthday = Birthday(birthday)
        else:
            raise ValueError("Birthday already exists for this record.")

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
