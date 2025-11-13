from pathlib import Path
import pickle

from address_book import AddressBook
from notes import NotesBook


# Папка користувача для зберігання всіх даних помічника
DATA_DIR = Path.home() / ".assistant_data"

# Окремі файли для контактів і нотаток
CONTACTS_FILE = DATA_DIR / "contacts.bin"
NOTES_FILE = DATA_DIR / "notes.bin"

def ensure_data_dir():
    #Створює директорію для даних, якщо її ще немає.
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def save_data(data, file_path):
    #Зберегти будь-який об'єкт у файл через pickle.
    ensure_data_dir()
    with open(file_path, "wb") as file:
        pickle.dump(data, file)


def load_data(file_path, factory):
    #Завантажити об'єкт із файлу.

    #Якщо файл не існує або пошкоджений — повернути factory().

    if not file_path.exists():
        return factory()

    try:
        with open(file_path, "rb") as file:
            return pickle.load(file)
    except Exception:
        return factory()


# ---------- КОНТАКТИ ----------

def load_address_book():
    #Завантажити книгу контактів або створити нову.
    return load_data(CONTACTS_FILE, AddressBook)


def save_address_book(book):
    #Зберегти книгу контактів у файл.
    save_data(book, CONTACTS_FILE)


# ---------- НОТАТКИ ----------

def load_notes_book():
    #Завантажити книгу нотаток або створити нову.
    return load_data(NOTES_FILE, NotesBook)


def save_notes_book(book):
    #Зберегти книгу нотаток у файл.
    save_data(book, NOTES_FILE)
