import sys
import os
import difflib
try:
    from prompt_toolkit import PromptSession
    from prompt_toolkit.completion import WordCompleter, FuzzyCompleter
except Exception:
    PromptSession = None
    WordCompleter = None
    FuzzyCompleter = None

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
    search_names,
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
    'find-note-by-id'       : find_note_by_id,
    'remove-tag-from-note'  : remove_tag_from_note,
    'edit-tag-in-note'      : edit_tag_in_note
}

HELPER_COMMANDS = {
    "hello"         : show_help,
    "close"         : exit_assistant,
    "exit"          : exit_assistant,
    "wrong-command" : wrong_command
}

ADDR_BOOK_COMMANDS = {
    'add-contact'   : add_contact,
    'change-phone'  : change_phone,
    'show-phone'    : show_phone,
    'show-all'      : show_all_contacts,
    'search'        : search_names,
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

    # prepare interactive autocompletion session if prompt_toolkit is available
    session = None
    if PromptSession is not None:
        # build list of command aliases for completion
        command_keys = list(ADDR_BOOK_COMMANDS.keys()) + list(NOTES_COMMANDS.keys()) + list(HELPER_COMMANDS.keys())
        aliases = set()
        for c in command_keys:
            aliases.add(c)
            aliases.add(c.replace('-', ' '))
            aliases.add(c.replace('-', ''))
            aliases.add(c.replace('-', '_'))
        # create a fuzzy completer so suggestions appear as a dropdown while typing
        word_completer = WordCompleter(sorted(aliases), ignore_case=True, match_middle=True)
        fuzzy = FuzzyCompleter(word_completer)
        session = PromptSession(completer=fuzzy)

    try:
        while True:
            # read input using prompt_toolkit if available (shows dropdown suggestions)
            if session is not None:
                try:
                    user_input = session.prompt("Enter a command: ")
                except KeyboardInterrupt:
                    # allow ctrl-c to break out of prompt
                    print()
                    continue
            else:
                user_input = input("Enter a command: ")
            # avoid crash if empty input
            if not user_input.strip():
                print("Please enter a command")
                continue

            command, *args = parse_input(user_input)

            # if command in ADDR_BOOK_COMMANDS.keys():
            #     print(ADDR_BOOK_COMMANDS[command](book, *args))

            # elif command in NOTES_COMMANDS.keys():
            #     print(NOTES_COMMANDS[command](notes_book, *args))

            # elif command in HELPER_COMMANDS.keys():
            #     print(HELPER_COMMANDS[command](*args))

            # Build combined commands map for guessing
            ALL_COMMANDS = {**ADDR_BOOK_COMMANDS, **NOTES_COMMANDS, **HELPER_COMMANDS}

            if command in ADDR_BOOK_COMMANDS.keys():
                # helper: normalize candidate forms to increase match robustness
                def canonical_forms(cmd_key: str):
                    forms = {cmd_key}
                    forms.add(cmd_key.replace('-', ' '))
                    forms.add(cmd_key.replace('-', ''))
                    forms.add(cmd_key.replace('-', '_'))
                    return forms

                # compute best match using SequenceMatcher over whole input and first token
                def guess_command(text: str):
                    text = (text or "").strip().lower()
                    if not text:
                        return None, 0.0

                    token = text.split()[0]
                    best = (None, 0.0)
                    for c in ALL_COMMANDS.keys():
                        # check multiple canonical forms for the command key
                        for form in canonical_forms(c):
                            score_token = difflib.SequenceMatcher(None, token, form).ratio()
                            score_full = difflib.SequenceMatcher(None, text, form).ratio()
                            score = max(score_token, score_full)
                            if score > best[1]:
                                best = (c, score)

                    return best

                suggestion, score = guess_command(user_input)
                # threshold (tunable)
                if suggestion and score >= 0.6:
                    confirm = input(f"Did you mean '{suggestion}'? (y/n): ").strip().lower()
                    if confirm in ("y", "yes", ""):
                        # attempt to remove the matched alias from user_input to build args
                        aliases = list(canonical_forms(suggestion))
                        lowered = user_input.lower()
                        remainder = lowered
                        removed = False
                        for a in sorted(aliases, key=len, reverse=True):
                            if remainder.startswith(a):
                                remainder = remainder[len(a):].strip()
                                removed = True
                                break
                            idx = remainder.find(a)
                            if idx != -1:
                                remainder = (remainder[:idx] + remainder[idx+len(a):]).strip()
                                removed = True
                                break

                        exec_args = remainder.split() if remainder else args

                        if suggestion in ADDR_BOOK_COMMANDS:
                            print(ADDR_BOOK_COMMANDS[suggestion](book, *exec_args))
                        elif suggestion in NOTES_COMMANDS:
                            print(NOTES_COMMANDS[suggestion](notes_book, *exec_args))
                        elif suggestion in HELPER_COMMANDS:
                            print(HELPER_COMMANDS[suggestion](*exec_args))
                        else:
                            print("Unknown command")
                    else:
                        print("Unknown command")
                else:
                    print("Unknown command")

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