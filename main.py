import sys
import os

path = os.path.split(os.path.abspath(__file__)) # Get current script's directory
target_dir =path[0] + os.sep + 'include' # Go up one level and then into 'utils'
# Add the directory to sys.path
sys.path.append(target_dir)

from notes_handlers import (
    add_note, edit_note,
    delete_note,
    show_all_notes,
    find_note_by_id,
    remove_tag_from_note,
    edit_tag_in_note
)
from address_handlers import (
    add_contact,
    change_contact,
    show_phone,
    show_all_contacts,
    search_names,
    add_email_cmd,
    change_email_cmd,
    delete_email_cmd,
    show_email_cmd,
    add_birthday,
    show_birthday
)
from storage import (
    load_notes_book,
    save_notes_book,
    load_address_book,
    save_address_book
)
from utils import parse_input

not_found_message = "Contact does not exist, you can add it"

#@input_error

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def main():
    # Завантажуємо книги контактів і нотаток
    book = load_address_book() #Завантаження Контактів.
    notes_book = load_notes_book() #Завантаження Контактів.

    print("Welcome to the assistant bot!")

    try:
        while True:
            user_input = input("Enter a command: ")
            command, *args = parse_input(user_input)

            match command:
                case "hello":
                    print("How can I help you?")
                case "close" | "exit":
                    # Зберігаємо книги контактів і нотаток
                    save_address_book(book) #Збереження Контактів.
                    save_notes_book(notes_book) #Збереження Нотаток.

                    break

                case "add":
                    print(add_contact(args, book))
                case "change":
                    print(change_contact(args, book))
                case "phone":
                    print(show_phone(args, book))
                case "all":
                    print(show_all_contacts(args, book))
                
                case "search":
                    print(search_names(args, book))

                # Email
                case "add-email":
                    print(add_email_cmd(args, book))
                case "change-email":
                    print(change_email_cmd(args, book))
                case "delete-email":
                    print(delete_email_cmd(args, book))
                case "show-email":
                    print(show_email_cmd(args, book))

                # Days & birthdays
                case "add-birthday":
                    print(add_birthday(args, book))
                case "show-birthday":
                    print(show_birthday(args, book))
                case "birthdays":
                    print(book.get_upcoming_birthdays())
                case "add-note":

                #Notes
                    print(add_note(args, notes_book))
                case "edit-note":
                    print(edit_note(args, notes_book))
                case "delete-note":
                    print(delete_note(args, notes_book))
                case "all-notes":
                    print(show_all_notes(notes_book))
                case "note-by-id":
                    print(find_note_by_id(args, notes_book))
                case "remove-tag":
                    print(remove_tag_from_note(args, notes_book))
                case "edit-tag":
                    print(edit_tag_in_note(args, notes_book))
                
                case _:
                    print("Invalid command.")
    except KeyboardInterrupt:
        # Якщо користувач натиснув Ctrl+C — теж зберігаємо
        save_address_book(book)
        save_notes_book(notes_book)

    finally:
        # зберігаємо у будь-якому разі
        save_address_book(book)
        save_notes_book(notes_book)

    print("\nGood bye!")

if __name__ == "__main__":
    main()