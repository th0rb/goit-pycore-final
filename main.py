import sys
import os

path = os.path.split(os.path.abspath(__file__)) # Get current script's directory
target_dir =path[0] + os.sep + 'include' # Go up one level and then into 'utils'
# Add the directory to sys.path
sys.path.append(target_dir) 


from adress_book import AddressBook
from error import input_error
from record import Record
from storage import load_data, save_data, DEFAULT_FILENANE
import sys

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
        # перевірка: цей номер не має використовуватися іншим контактом
        if book.is_phone_taken(phone, exclude_name=name):
            return "Phone is already used by another contact."
        record.add_phone(phone)

    return message


@input_error
def change_contact(args, book: AddressBook):
    if len(args) != 3:
        return "Invalid number of arguments. Usage: change [name] [old_number] [new_number]"

    name, old_number, new_number = args
    record = book.find(name)
    if record is None:
        return not_found_message

    #  перевірка: новий номер не має використовуватися іншим контактом
    if book.is_phone_taken(new_number, exclude_name=name):
        return "Phone is already used by another contact."

    record.edit_phone(old_number, new_number)
    return "Phone changed"

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
def add_email_cmd(args, book):
    # usage: add-email <name> <email>
    name, email = args
    record = book.find(name)

    if record is None:
        from include.record import Record
        record = Record(name)
        book.add_record(record)

    # емейл не повинен існувати в ІНШОГО контакту
    if book.is_email_taken(email, exclude_name=name):
        return "Email is already used by another contact."

    record.add_email(email)
    return "Email added."


@input_error
def change_email_cmd(args, book):
    # usage: change-email <name> <old_email> <new_email>
    name, old_e, new_e = args
    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found")

    #  новий емейл не повинен існувати в ІНШОГО контакту
    if book.is_email_taken(new_e, exclude_name=name):
        return "Email is already used by another contact."

    record.edit_email(old_e, new_e)
    return "Email updated."


@input_error
def delete_email_cmd(args, book):
    # usage: delete-email <name> <email>
    name, e = args
    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found")

    record.remove_email(e)
    return "Email deleted."


@input_error
def show_email_cmd(args, book):
    (name,) = args
    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found")
    emails = "; ".join(e.value for e in record.emails) if record.emails else "-"
    return f"{name}: {emails}"

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


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def main():

    if len(sys.argv) > 1:
        contacts_file = sys.argv[1]
    else:
        contacts_file = DEFAULT_FILENANE
    book = load_data(contacts_file)

    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        match command:
            case "hello":
                print("How can I help you?")
            case "close" | "exit":
                save_data(book, contacts_file)
                print("Good bye!")
                break
            case "add":
                print(add_contact(args, book))
            case "change":
                print(change_contact(args, book))
            case "phone":
                print(show_phone(args, book))
            case "add-email":
                print(add_email_cmd(args, book))
            case "change-email":
                print(change_email_cmd(args, book))
            case "delete-email":
                print(delete_email_cmd(args, book))
            case "show-email":
                print(show_email_cmd(args, book))    
            case "all":
                print(show_all_contacts(args, book))
            case "add-birthday":
                print(add_birthday(args, book))
            case "show-birthday":
                print(show_birthday(args, book))
            case "birthdays":
                print(book.get_upcoming_birthdays())
            case _:
                print("Invalid command.")


if __name__ == "__main__":
    main()