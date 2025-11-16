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


    def add_email(self, value: str) -> None:
        if any(e.value == value for e in self.emails):
            raise ValueError("Такий email уже є в цьому контакті.")
        self.emails.append(Email(value))

    def find_email(self, value: str) -> "Email | None":
        return next((e for e in self.emails if e.value == value), None)

    def edit_email(self, old_value: str, new_value: str) -> None:
        email_obj = self.find_email(old_value)
        if not email_obj:
            raise KeyError("Email не знайдено в цьому контакті.")
        if any(e.value == new_value for e in self.emails if e is not email_obj):
            raise ValueError("Такий email уже є в цьому контакті.")
        idx = self.emails.index(email_obj)
        self.emails[idx] = Email(new_value)

    def remove_email(self, value: str) -> None:
        email_obj = self.find_email(value)
        if not email_obj:
            raise KeyError("Email не знайдено в цьому контакті.")
        self.emails.remove(email_obj)

    def add_phone(self, phone_number: str) -> None:
        if any(p.value == phone_number for p in self.phones):
            raise ValueError("Такий номер уже є в цьому контакті.")
        self.phones.append(Phone(phone_number))

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        phone = self.find_phone(old_phone)
        if not phone:
            raise KeyError("Номер не знайдено в цьому контакті.")
        if any(p.value == new_phone for p in self.phones if p is not phone):
            raise ValueError("Такий номер уже є в цьому контакті.")
        idx = self.phones.index(phone)
        self.phones[idx] = Phone(new_phone)

    def remove_phone(self, phone_number: str) -> None:
        phone = self.find_phone(phone_number)
        if not phone:
            raise KeyError("Номер не знайдено в цьому контакті.")
        self.phones.remove(phone)

    def find_phone(self, phone_number: str) -> Phone | None:
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
        # Ім'я 
        contact_str = f"Contact: | {self.name.value:<20}"

        # Телефони
        if self.phones:
            phones_str = ", ".join(p.value for p in self.phones)
            contact_str += f" | {phones_str}"

        # Email-и
        if hasattr(self, "emails") and self.emails:
            emails_str = ", ".join(e.value for e in self.emails)
            contact_str += f" | {emails_str} |"

        return contact_str
