import sys
import os

path = os.path.split(os.path.abspath(__file__)) # Get current script's directory
target_dir =path[0] + os.sep + 'include' # Go up one level and then into 'utils'
# Add the directory to sys.path
sys.path.append(target_dir) 


from include.address_book import AddressBook
from include.error import input_error
from include.record import Record
from include.storage import (
    load_address_book,
    save_address_book,
    load_notes_book,
    save_notes_book
)


not_found_message = "Contact does not exist, you can add it"

ADDR_BOOK_COMMANDS = {
    "hello" : "show_help", 
    "close" : "exit_assistant",
    "exit" : "exit_assistant",
    "add" : "add_contact",
    "change" : "change_contact",
    "phone" : "show_phone",
    "all" : "show_all_contacts",
    "add-email" : "add_email",
    "change-email" : "change_email",
    "delete-email" : "delete_email",
    "show-email" : "show_email",
    "add-birthday": "add_birthday",
    "show-birthday" : "show_upcoming_birthdays",
}

def show_help(book: AddressBook):
    return "TODO: show nice help page"

def exit_assistant(book: AddressBook):
    save_address_book(book)
    print ("\nGood bye!")
    sys.exit()

def show_upcoming_birthdays(book: AddressBook):
    return book.get_upcoming_birthdays()


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
def change_contact(book: AddressBook, *args):
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
def show_email_cmd(book: AddressBook, *args):
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


def parse_input(user_input):
    if not user_input:
        return '', None
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def assistant():
    # Завантажуємо книги контактів і нотаток
    book = load_address_book() #Завантаження Контактів.
    #notes_book = load_notes_book() #Завантаження Контактів.

    print("Welcome to the assistant bot!")

    try:
        while True:
            user_input = input("Enter a command: ")
            command, *args = parse_input(user_input)

            if command in ADDR_BOOK_COMMANDS.keys():
                call_func = globals()[ADDR_BOOK_COMMANDS[command]]
                print(call_func(book, *args))
            else:
                print("Invalid command.")

    except KeyboardInterrupt:
        # Якщо користувач натиснув Ctrl+C — теж зберігаємо
        save_address_book(book)
        #save_notes_book(notes_book)

    finally:
        # зберігаємо у будь-якому разі
        save_address_book(book)
        #save_notes_book(notes_book)

    print("\nGood bye!")

if __name__ == "__main__":
    assistant()