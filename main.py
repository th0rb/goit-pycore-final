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
    change_phone,
    show_phone,
    show_all_contacts,
    search,
    add_email,
    change_email,
    delete_email,
    show_email,
    add_birthday,
    show_birthday
)
from storage import (
    load_notes_book,
    save_notes_book,
    load_address_book,
    save_address_book
)

from help_handlers import (
    show_help,
    exit_assistant,
    wrong_command
)

from utils import parse_input

not_found_message = "Contact does not exist, you can add it"

#@input_error

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

NOTES_COMMANDS = {
    'add-note'              : add_note, 
    'edit-note'             : edit_note,
    'delete-note'           : delete_note,
    'show-all-notes'        : show_all_notes,
    'find_note-by-id'       : find_note_by_id,
    'remove-tag-from-note'  : remove_tag_from_note,
    'edit-tag-in-notee'     : edit_tag_in_note
}

HELPER_COMMANDS = {
    "hello"         : show_help,
    "close"         : exit_assistant,
    "exit"          : exit_assistant,
    "wrong_command" : wrong_command
}

ADDR_BOOK_COMMANDS = {
    'add-contact'   : add_contact,
    'change-phone'  : change_phone,
    'show-phone'    : show_phone,
    'show-all'      : show_all_contacts,
    'search'        : search,
    'add-email'     : add_email,
    'change-email'  : change_email,
    'delete-email'  : delete_email,
    'show-email'    : show_email,
    'add-birthday'  : add_birthday,
    'show-birthday' : show_birthday
}


def main():
    # Завантажуємо книги контактів і нотаток
    book = load_address_book()
    notes_book = load_notes_book()

    print("Welcome to the assistant bot!")

    try:
        while True:
            user_input = input("Enter a command: ")
            command, *args = parse_input(user_input)

            if command in ADDR_BOOK_COMMANDS.keys():
                print (ADDR_BOOK_COMMANDS[command](book, *args))

            elif command in NOTES_COMMANDS.keys():
                print (NOTES_COMMANDS[command](notes_book, *args))

            elif command in HELPER_COMMANDS.keys():
                print (HELPER_COMMANDS[command](*args))
            
            else:
                print ("Unknown command")

    except KeyboardInterrupt:
        # Якщо користувач натиснув Ctrl+C
        print ("Interrupted!")

    finally:
        # зберігаємо у будь-якому разі
        save_address_book(book)
        save_notes_book(notes_book)
        print("\nGood bye!")

if __name__ == "__main__":
    main()