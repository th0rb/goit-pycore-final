from pathlib import Path
import json

from address_book import AddressBook
from notes_book import NotesBook

from record import Record
from note import Note
from note_tag import NoteTag

# Папка користувача для зберігання всіх даних помічника
DATA_DIR = Path.home() / ".assistant_data"

# Окремі файли для контактів і нотаток (формат JSON)
CONTACTS_FILE = DATA_DIR / "contacts.json"
NOTES_FILE = DATA_DIR / "notes.json"

def ensure_data_dir() -> None:
    #Створює директорію для даних, якщо її ще немає.
    DATA_DIR.mkdir(parents=True, exist_ok=True)

#СЕРІАЛІЗАЦІЯ / ДЕСЕРІАЛІЗАЦІЯ КОНТАКТІВ

def address_book_to_json(book: AddressBook) -> dict:
    #Перетворює AddressBook у структуру, яка може бути збережена в JSON.

    contacts = []

    for _, record in book.data.items():
        contact_data = {
            "name": record.name.value,
            "phones": [phone.value for phone in record.phones],
            "emails": [email.value for email in record.emails],
            "birthday": None,
        }

        if record.birthday:
            # Використовуємо __str__, щоб отримати дату у форматі DD.MM.YYYY
            contact_data["birthday"] = str(record.birthday)

        contacts.append(contact_data)

    return {"contacts": contacts}

def address_book_from_json(data: dict) -> AddressBook:
    #Відновлює AddressBook зі структури, прочитаної з JSON.

    book = AddressBook()
    contacts = data.get("contacts", [])

    for item in contacts:
        name = item.get("name")
        if not name:
            continue

        record = Record(name)

        # Телефони
        for phone in item.get("phones", []):
            try:
                record.add_phone(phone)
            except ValueError:
                # Пропускаємо некоректні номери
                continue

        # Email-и
        for email in item.get("emails", []):
            try:
                record.add_email(email)
            except ValueError:
                # Пропускаємо некоректні email-и
                continue

        # День народження
        birthday_str = item.get("birthday")
        if birthday_str:
            try:
                record.add_birthday(birthday_str)
            except ValueError:
                # Пропускаємо некоректні дати
                pass

        try:
            book.add_record(record)
        except KeyError:
            # Якщо контакт з таким ім'ям уже є — пропускаємо
            continue

    return book

#СЕРІАЛІЗАЦІЯ / ДЕСЕРІАЛІЗАЦІЯ НОТАТОК

def notes_book_to_json(notes_book: NotesBook) -> dict:
    #Перетворює NotesBook у структуру, яка може бути збережена в JSON.

    notes = []

    for note in notes_book.data.values():
        note_data = {
            "id": note.id,
            "text": note.note_text.value,
            "tags": [tag.value for tag in note.note_tags],
        }
        notes.append(note_data)

    return {"notes": notes}


def notes_book_from_json(data: dict) -> NotesBook:
    #Відновлює NotesBook зі структури, прочитаної з JSON.
    
    book = NotesBook()
    notes = data.get("notes", [])

    for item in notes:
        text = item.get("text", "")
        if not text.strip():
            continue

        # Створюємо Note, використовуючи існуючу логіку в класі Note
        note = Note(text)

        # Відновлюємо збережений id (Note зберігає його у приватному полі)
        stored_id = item.get("id")
        if stored_id:
            try:
                setattr(note, "_Note__id", stored_id)
            except Exception:
                # Якщо щось пішло не так — залишаємо згенерований id
                pass

        # Теги
        for tag_value in item.get("tags", []):
            try:
                note.note_tags.append(NoteTag(tag_value))
            except ValueError:
                # Пропускаємо некоректні теги
                continue

        try:
            book.add_note(note)
        except KeyError:
            # Якщо є дублікат по тексту — пропускаємо
            continue

    return book

#ЗАГАЛЬНІ ФУНКЦІЇ ЗАВАНТАЖЕННЯ / ЗБЕРЕЖЕННЯ

def load_address_book() -> AddressBook:
    #Завантажити книгу контактів або створити нову.
    
    ensure_data_dir()
    if not CONTACTS_FILE.exists():
        return AddressBook()

    try:
        with CONTACTS_FILE.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
        return address_book_from_json(data)
    except (json.JSONDecodeError, OSError):
        # Пошкоджений файл або проблеми читання — повертаємо порожню книгу
        return AddressBook()

def save_address_book(book: AddressBook) -> None:
    #Зберегти книгу контактів у JSON-файл.
    
    ensure_data_dir()
    data = address_book_to_json(book)
    with CONTACTS_FILE.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)

def load_notes_book() -> NotesBook:
    #Завантажити книгу нотаток або створити нову.

    ensure_data_dir()

    if not NOTES_FILE.exists():
        return NotesBook()

    try:
        with NOTES_FILE.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
        return notes_book_from_json(data)
    except (json.JSONDecodeError, OSError):
        # Пошкоджений файл або проблеми читання — повертаємо порожню книгу
        return NotesBook()

def save_notes_book(notes_book: NotesBook) -> None:
    #Зберегти книгу нотаток у JSON-файл.
    ensure_data_dir()
    data = notes_book_to_json(notes_book)
    with NOTES_FILE.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
