from error import input_error
from address_book import AddressBook
from record import Record

not_found_message = "Contact does not exist, you can add it"

@input_error
def add_contact(book: AddressBook, *args):
    name, phone = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        if book.is_phone_taken(phone):
            return "Цей номер уже використовується іншим контактом."
        record.add_phone(phone)
    return message


@input_error
def change_phone(book: AddressBook, *args):
    if len(args) != 3:
        return 'Invalid number of arguments. Usage: change [name] [old_number] [new_number]'
    name, old_number, new_number = args
    record = book.find(name)
    if record is None:
        return not_found_message
    if old_number == new_number:
        return "Змін немає (старий і новий номер однакові)."
    if book.is_phone_taken(new_number):
        return "Цей номер уже використовується іншим контактом."
    record.edit_phone(old_number, new_number)
    return "Номер змінено."


@input_error
def show_phone(book: AddressBook, *args):
    if len(args) != 1:
        return "Invalid number of arguments. Usage: phone [name]"
    name = args[0]
    record = book.find(name)
    if record is None:
        return not_found_message
    return record

@input_error
def show_all_contacts(book: AddressBook):
    if len(book) == 0:
        return "Address book is empty."
    contacts = "\n".join([str(record) for record in book.values()])
    return contacts

@input_error
def search(book: AddressBook, *args):
    if not args:
        return "Invalid number of arguments. Usage: search [text]"
    
    # Підтримуємо пошук за кількома словами: search John Doe
    query = " ".join(args).lower()

    # Визначаємо, чи запит схожий на email
    is_email_query = False
    if " " not in query and "@" in query:
        local_part, _, domain_part = query.partition("@")
        if local_part and "." in domain_part:
            is_email_query = True

    matches = []
    for record in book.values():
        # ----- ПОШУК ПО ІМЕНІ (завжди) -----
        if query in record.name.value.lower():
            matches.append(record.name.value)
            continue

        if is_email_query:
            # ----- ЗАПИТ СХОЖИЙ НА EMAIL → ШУКАЄМО ПО EMAIL -----
            emails = getattr(record, "emails", [])
            for email in emails:
                if query in email.value.lower():
                    matches.append(record.name.value)
                    break
        else:
            # ----- НЕ EMAIL → ШУКАЄМО ПО ТЕЛЕФОНУ -----
            phones = getattr(record, "phones", [])
            for phone in phones:
                if query in phone.value:
                    matches.append(record.name.value)
                    break

    if not matches:
        return "No contacts found for this query."

    # Формуємо нормальний вивід
    result = []
    for record in book.values():
        if record.name.value in matches:
            result.append(str(record))

    return "\n".join(result)

@input_error
def add_email(book: AddressBook, *args):
    name, email = args
    record = book.find(name)
    if record is None:
        record = Record(name)
        book.add_record(record)
    if book.is_email_taken(email):
        return "Цей email уже використовується іншим контактом."
    record.add_email(email)
    return "Email додано."

@input_error
def change_email(book: AddressBook, *args):
    name, old_e, new_e = args
    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found")
    if old_e == new_e:
        return "Змін немає (старий і новий email однакові)."
    if book.is_email_taken(new_e):
        return "Цей email уже використовується іншим контактом."
    record.edit_email(old_e, new_e)
    return "Email оновлено."

@input_error
def delete_email(book: AddressBook, *args):
    name, e = args
    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found")
    record.remove_email(e)
    return "Email видалено."

@input_error
def show_email(book: AddressBook, *args):
    name, = args
    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found")
    return "; ".join(e.value for e in record.emails) if record.emails else "У контакту немає жодного email."


@input_error
def add_birthday(book: AddressBook, *args):
    if len(args) != 2:
        return "Invalid number of arguments. Usage: add-birthday [name] [date]"
    name, date = args
    record = book.find(name)
    if record:
        record.add_birthday(date)
        return "Birthday added."
    else:
        return not_found_message
    
@input_error
def show_birthday(book: AddressBook, *args):
    if len(args) != 1:
        return "Invalid number of arguments. Usage: show-birthday [name]"
    name = args[0]
    record = book.find(name)
    if record:
        if record.birthday:
            return record.birthday
        else:
            return "Birthday not added to this contact."
    else:
        return not_found_message