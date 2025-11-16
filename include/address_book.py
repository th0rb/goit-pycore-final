from collections import UserDict
from record import Record


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
