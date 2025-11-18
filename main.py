import sys
import os
import difflib
import re
try:
    from prompt_toolkit import PromptSession
    from prompt_toolkit.completion import WordCompleter
except Exception:
    PromptSession = None
    WordCompleter = None
    FuzzyCompleter = None
from colorama import init, Fore, Back, Style
init(autoreset=True)

path = os.path.split(os.path.abspath(__file__)) # Get current script's directory
target_dir =path[0] + os.sep + 'include' # Go up one level and then into 'utils'
# Add the directory to sys.path
sys.path.append(target_dir)

from notes_handlers import (
    add_note,
    edit_note,
    delete_note,
    show_all_notes,
    find_note_by_id,
    remove_tag_from_note,
    edit_tag_in_note,
    search_notes_by_text,
    sort_notes_by_tags,
    search_notes_by_tags
)
from address_handlers import (
    add_contact,
    delete_contact,
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
    wrong_command,
    welcome_message
)

from birthday_handlers import show_upcoming_birthdays

from utils import parse_input

not_found_message = "Contact does not exist, you can add it"

NOTES_COMMANDS = {
    'add-note'              : add_note,
    'edit-note'             : edit_note,
    'delete-note'           : delete_note,
    'show-all-notes'        : show_all_notes,
    'find-note-by-id'       : find_note_by_id,
    'note-remove-tag'       : remove_tag_from_note,
    'note-edit-tag'         : edit_tag_in_note,
    'search-notes'          : search_notes_by_text,
    'search-notes-by-tags'  : search_notes_by_tags,
    'sort-notes-by-tags'    : sort_notes_by_tags,
}

HELPER_COMMANDS = {
    "hello"         : show_help,
    "help"          : show_help,
    "close"         : exit_assistant,
    "exit"          : exit_assistant,
}

ADDR_BOOK_COMMANDS = {
    'add-contact'   : add_contact,
    'delete-contact': delete_contact,
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

    welcome_message()
    show_upcoming_birthdays(book)

    def build_session():
        if PromptSession is None or WordCompleter is None:
            return None
        command_keys = list(ADDR_BOOK_COMMANDS.keys()) + list(NOTES_COMMANDS.keys()) + list(HELPER_COMMANDS.keys())

        aliases = set(command_keys)

        completer = WordCompleter(sorted(aliases), ignore_case=True, match_middle=False, sentence=True)
        return PromptSession(completer=completer)

    def canonical_forms(cmd_key: str):
        forms = {cmd_key, cmd_key.replace('-', ' '), cmd_key.replace('-', ''), cmd_key.replace('-', '_')}
        return forms

    def guess_command(text: str):
        text = (text or '').strip().lower()
        if not text:
            return None, 0.0
        token = text.split()[0]
        ALL_COMMANDS = {**ADDR_BOOK_COMMANDS, **NOTES_COMMANDS, **HELPER_COMMANDS}
        best = (None, 0.0)
        for c in ALL_COMMANDS.keys():
            for form in canonical_forms(c):
                score_token = difflib.SequenceMatcher(None, token, form).ratio()
                score_full = difflib.SequenceMatcher(None, text, form).ratio()
                score = max(score_token, score_full)
                if score > best[1]:
                    best = (c, score)
        return best

    def execute_suggestion(suggestion: str, exec_args: list[str]):
        if suggestion in ADDR_BOOK_COMMANDS:
            return ADDR_BOOK_COMMANDS[suggestion](book, *exec_args)
        if suggestion in NOTES_COMMANDS:
            return NOTES_COMMANDS[suggestion](notes_book, *exec_args)
        if suggestion in HELPER_COMMANDS:
            # helpers usually take no args; if exec_args is empty call without args
            if exec_args:
                return HELPER_COMMANDS[suggestion](*exec_args)
            return HELPER_COMMANDS[suggestion]()
        return 'Unknown command'

    session = build_session()

    try:
        while True:
            # read input using prompt_toolkit if available (shows dropdown suggestions)
            if session is not None:
                user_input = session.prompt('Enter a command: ')
            else:
                user_input = input('Enter a command: ')

            if not user_input.strip():
                wrong_command()
                continue

            command, *args = parse_input(user_input)

            # direct match
            if command in ADDR_BOOK_COMMANDS:
                print(ADDR_BOOK_COMMANDS[command](book, *args))
                continue
            if command in NOTES_COMMANDS:
                print(NOTES_COMMANDS[command](notes_book, *args))
                continue
            if command in HELPER_COMMANDS:
                print(HELPER_COMMANDS[command](*args))
                continue

            suggestion, score = guess_command(user_input)
            if suggestion and score >= 0.6:
                suggested_cmd = f"{suggestion}"
                print(f"Можливо ви мали на увазі: {Fore.YELLOW}{suggested_cmd}{Style.RESET_ALL}")

                confirm = input("Підтвердити команду? (y/n):").strip().lower()

                if confirm in ('y', 'yes'):
                    # Show suggested command as a prefill and allow the user to edit it.
                    prefill = f"{suggestion} {' '.join(args)}".strip()
                    resp = input(f"{Fore.YELLOW}Suggested: {Style.RESET_ALL} {prefill}\nPress Enter to accept or type corrected command: ").strip()
                    final_input = resp if resp else prefill
                    cmd, *new_args = parse_input(final_input)

                    # If user edited the command name, run that command directly if it exists.
                    if cmd in ADDR_BOOK_COMMANDS:
                        print(ADDR_BOOK_COMMANDS[cmd](book, *new_args))
                    elif cmd in NOTES_COMMANDS:
                        print(NOTES_COMMANDS[cmd](notes_book, *new_args))
                    elif cmd in HELPER_COMMANDS:
                        print(HELPER_COMMANDS[cmd](*new_args))
                    else:
                        # Otherwise assume they accepted the suggested command and pass args.
                        print(execute_suggestion(suggestion, new_args))
                else:
                    print("Дія скасована користувачем.")
            else:
                wrong_command()

    except KeyboardInterrupt:
        exit_assistant()

    finally:
        save_address_book(book)
        save_notes_book(notes_book)

    exit_assistant()

if __name__ == "__main__":
    main()