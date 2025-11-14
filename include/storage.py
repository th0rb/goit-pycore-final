import pickle
from enum import Enum
from adress_book import AddressBook
from notes_book import NotesBook

DEFAULT_FILENANE = "contacts.pkl"
NOTES_FILENAME = "notes.pkl"

class Mode(Enum):
    ADDRESS_BOOK = 'address_book'
    NOTES_BOOK = 'notes_book'

def save_data(data, filename=DEFAULT_FILENANE):
    with open(filename, "wb") as f:
        pickle.dump(data, f)

def load_data(filename=DEFAULT_FILENANE, mode=Mode.ADDRESS_BOOK.value) -> AddressBook | NotesBook:
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        if mode == Mode.ADDRESS_BOOK.value:
            return AddressBook()  # Повернення нової адресної книги, якщо файл не знайдено
        if mode == Mode.NOTES_BOOK.value:
            return NotesBook()  # Повернення нової книги нотаток, якщо файл не знайдено