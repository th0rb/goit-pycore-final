import sys
from colorama import init, Fore, Style

init(autoreset=True)

# Для кольорів
TITLE = Fore.MAGENTA + Style.BRIGHT
CMD = Fore.YELLOW + Style.BRIGHT
DESC = Fore.CYAN
RESET = Style.RESET_ALL
ERROR = Fore.RED + Style.BRIGHT
GOODBYE = Fore.GREEN + Style.BRIGHT
INFO = Fore.CYAN


def show_help():
    print(TITLE + "\n📘 AVAILABLE COMMANDS\n")

    # -----------------------------------------------------
    # 1️⃣ Assistant Commands
    # -----------------------------------------------------
    assistant = [
        ("hello / help", "Show this help"),
        ("exit / close", "Exit assistant"),
    ]

    # -----------------------------------------------------
    # 2️⃣ Address Book Commands
    # -----------------------------------------------------
    address_book = [
        ("add-contact", "Add a new contact"),
        ("change-contact", "Change phone/email for a contact"),
        ("show-phone", "Show contact's phone number"),
        ("show-all", "Show all saved contacts"),
        ("add-email", "Attach email to contact"),
        ("change-email", "Replace contact email"),
        ("delete-email", "Remove email from contact"),
        ("show-email", "Show all emails for contact"),
        ("add-birthday", "Add birthday date"),
        ("show-birthday", "Show contact birthday"),
    ]

    # -----------------------------------------------------
    # 3️⃣ Notes Commands
    # -----------------------------------------------------
    notes = [
        ("add-note", "Create a new note"),
        ("edit-note", "Edit existing note"),
        ("delete-note", "Remove note"),
        ("show-all-notes", "List all notes"),
        ("find_note-by-id", "Search note by ID"),
        ("remove-tag-from-note", "Delete tag from note"),
        ("edit-tag-in-note", "Edit tag of note"),
    ]

    # -----------------------------------------------------
    # Функція для малювання таблиці
    # -----------------------------------------------------
    def draw_table(title, emoji, commands):
        print(TITLE + f"\n{emoji} {title}\n")

        top =    f"{Fore.MAGENTA}╔════════════════════════════╦══════════════════════════════════════════════╗"
        header = f"{Fore.MAGENTA}║ {'Command':<26} ║ {'Description':<44} ║"
        mid =    f"{Fore.MAGENTA}╠════════════════════════════╬══════════════════════════════════════════════╣"
        bottom = f"{Fore.MAGENTA}╚════════════════════════════╩══════════════════════════════════════════════╝"

        print(top)
        print(header)
        print(mid)

        for cmd, desc in commands:
            print(f"║ {CMD}{cmd:<26}{RESET} ║ {DESC}{desc:<44}{RESET} ║")

        print(bottom)

    # 🔥 Малюємо три секції:
    draw_table("Assistant Commands", "🤖", assistant)
    draw_table("Address Book Commands", "📒", address_book)
    draw_table("Notes Commands", "📝", notes)

    return ""


def wrong_command():
    print(ERROR + "❌ Unknown command! Type 'hello' for help.")


def exit_assistant():
    print(GOODBYE + "\n👋 See you soon!\n")
    sys.exit()

def welcome_message():
    print(TITLE + "\n🤖 Welcome to your colorful assistant bot! 🎨\n")
    print(INFO + "🤖 If you need help, write Hello! \n")
