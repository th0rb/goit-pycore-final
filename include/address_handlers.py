from error import input_error
from address_book import AddressBook
from record import Record

not_found_message = "Contact does not exist, you can add it"

@input_error
def add_contact(args, book: AddressBook):
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
def change_contact(args, book: AddressBook):
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
def show_phone(args, book: AddressBook):
    if len(args) != 1:
        return "Invalid number of arguments. Usage: phone [name]"
    name = args[0]
    record = book.find(name)
    if record is None:
        return not_found_message
    return record

@input_error
def show_all_contacts(args, book: AddressBook):
    if len(book) == 0:
        return "Address book is empty."
    contacts = "\n".join([str(record) for record in book.values()])
    return contacts

@input_error
def add_email_cmd(args, book: AddressBook):
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
def change_email_cmd(args, book: AddressBook):
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
def delete_email_cmd(args, book: AddressBook):
    name, e = args
    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found")
    record.remove_email(e)
    return "Email видалено."

@input_error
def show_email_cmd(args, book: AddressBook):
    name, = args
    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found")
    return "; ".join(e.value for e in record.emails) if record.emails else "У контакту немає жодного email."


@input_error
def add_birthday(args, book: AddressBook):
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
def show_birthday(args, book: AddressBook):
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