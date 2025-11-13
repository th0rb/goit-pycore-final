import pickle
from address_book import AddressBook

DEFAULT_FILENANE = "contacts.pkl"

def save_data(book, filename=DEFAULT_FILENANE):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename=DEFAULT_FILENANE):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  # Повернення нової адресної книги, якщо файл не знайдено