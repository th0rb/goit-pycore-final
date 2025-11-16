# goit-pycore-final

Personal Assistant
Консольний застосунок для управління контактами та нотатками. Підтримує збереження даних, пошук, редагування, сортування та нагадування про дні народження.

МОЖЛИВОСТІ

Контакти:
- Додавання контактів
- Редагування телефонів та email
- Додавання та зміна дати народження
- Пошук за імʼям, email або телефоном
- Показ усіх контактів
- Видалення контактів
- Перевірка унікальності email / телефону
- Нагадування про дні народження

Нотатки:
- Додавання нотаток (з автоматичним коротким UUID)
- Пошук за текстом
- Пошук за тегами
- Редагування нотаток
- Видалення нотаток
- Сортування за тегами
- Додавання, редагування та видалення тегів

Збереження даних:
- Зберігаються у папці:
  ~/.assistant_data/contacts.bin
  ~/.assistant_data/notes.bin

Формат — pickle. При відсутності файлів — створюються порожні.
При будь-якому виході (exit, close, Ctrl+C) виконується збереження стану.

Валідація:
Телефон — 10 цифр.
Email — коректний формат (безпечна текстова валідація).

UI:
Кольоровий вивід через Colorama.
Зручні підказки (довідкова таблиця команд).

Пошук:
Контакти — за іменем, телефоном, email, частковим збігом.

Вимоги
Python 3.10+ (використовується match/case).
Рекомендовано віртуальне оточення.

Для кольорів: пакет colorama.

ВСТАНОВЛЕННЯ

1. Встановити залежності:
pip install -r requirements.txt

2. Запуск програми:
python main.py

Встановлення як пакет (опційно)
pip install -e .
assistant-bot   # якщо вказано console_scripts в проєкті

КОМАНДИ КОНТАКТІВ

Додати контакт:
add-contact [name] [phone] [email?]

Змінити телефон:
change-phone [name] [old_phone] [new_phone]

Показати телефони:
show-phone [name]

Додати email:
add-email [name] [email]

Змінити email:
change-email [name] [old_email] [new_email]

Видалити email:
delete-email [name] [email]

Додати або змінити день народження:
add-birthday [name] [DD.MM.YYYY]

Показати дату народження:
show-birthday [name]

Показати наближені дні народження:
birthdays

Показати всі контакти:
show-all

Видалити контакт:
delete-contact [name]

Пошук:
search [query]

КОМАНДИ КОНТАКТІВ

Додати контакт:
add-contact [name] [phone] [email?]

Змінити телефон:
change-phone [name] [old_phone] [new_phone]

Показати телефони:
show-phone [name]

Додати email:
add-email [name] [email]

Змінити email:
change-email [name] [old_email] [new_email]

Видалити email:
delete-email [name] [email]

Додати або змінити день народження:
add-birthday [name] [DD.MM.YYYY]

Показати дату народження:
show-birthday [name]

Показати наближені дні народження:
birthdays

Показати всі контакти:
show-all

Видалити контакт:
delete-contact [name]

Пошук:
search [query]

КОМАНДИ НОТАТОК

Додати нотатку:
add-note [text] [#tag1 #tag2 ...]

Редагувати нотатку:
edit-note [note_id] [new_text]

Видалити нотатку:
delete-note [note_id]

Знайти нотатку за ID:
find-note-by-id [note_id]

Показати всі нотатки:
show-all-notes

Пошук за текстом:
search-notes-by-text [text]

Пошук за тегами:
search-notes-by-tags [#tag1 #tag2]

Додати тег:
add-tag-to-note [note_id] [#tag]

Видалити тег:
remove-tag-from-note [note_id] [#tag]

Редагувати тег:
edit-tag-in-note [note_id] [old_tag] [new_tag]

Сортування нотаток за тегами:
sort-notes-by-tags

СИСТЕМНІ КОМАНДИ

Показати всі команди:
help

Вихід:
exit
close
quit

Кольоровий інтерфейс (Colorama)

Імена команд, успіх/помилка, заголовки таблиць — виділяються кольорами для зручності.
Щоб увімкнути кольори на Windows, використовується colorama.init().

Пошук
search <запит> шукає часткові співпадіння в імені, телефонах, email-ах.

Для нотаток доступний  за тегами (note-tags).

Структура (скорочено)
include/
  adress_book.py    # AddressBook: add/find/delete, унікальність, birthdays(N днів)
  record.py         # Record: Name, [Phone], [Email], Birthday; add/edit/remove/find
  phone.py          # Phone: 10 цифр (валідація)
  email.py          # Email: поле email (валідація формату)
  birthday.py       # Birthday: DD.MM.YYYY
  notes_book.py     # NotesBook: CRUD по нотатках + теги
  error.py          # декоратор input_error (читабельні повідомлення)
  storage.py        # DATA_DIR, CONTACTS_FILE, NOTES_FILE; save/load (pickle)
main.py             # CLI, парсер команд, match/case, збереження при exit/Ctrl+C

Розробка (workflow з форком)
Форк → клон свого форка.

Додати upstream:
git remote add upstream https://github.com/<owner>/goit-pycore-final.git
git fetch upstream

Працювати у гілці від develop (наприклад, feature/<name>).
Коміти → пуш у свій форк → Pull Request в upstream/develop.
Якщо upstream змінився — git fetch upstream && git merge upstream/develop у свою гілку.

Примітки
Валідація email/телефону — інтегрована; у разі помилок користувач отримує зрозуміле повідомлення.

ПРИКЛАД РОБОТИ
> add-contact John 0931234567 john@example.com
Contact 'John' added.

> add-email John john@example.com
Email added.

> phone John
John: 1234567890

> show-email John
john@example.com

> add-birthday John 12.04.1990
Birthday added for John.

> birthdays
Upcoming birthdays:
 • John — 12.04.1990

> exit
Good bye!

Проєкт виконаний у рамках курсу Python.