# goit-pycore-final
Assistant Bot (CLI)
Консольний асистент для роботи з контактами та нотатками. Підтримує телефони, email-и, дні народження, пошук за критеріями, нотатки з тегами. Усі дані зберігаються на диску в папці користувача та автоматично відновлюються при запуску. При виході через Ctrl+C стан також зберігається.

Можливості
Адресна книга: контакти, кілька телефонів та email-адрес у одному записі.
Глобальна унікальність: один і той самий телефон або email не можуть належати двом різним контактам.
Без дублів у межах контакту: повторні однакові телефон/email для одного запису блокуються з читабельними повідомленнями.

Дні народження:
Додавання/перегляд дня народження контакту.
Виведення списку контактів, у яких ДН через N днів від сьогодні (без перенесення вихідних на понеділок/вівторок).

Нотатки з тегами:
Додавання, редагування, видалення нотаток.
Додавання тегів до нотаток та фільтрація за тегами.

Збереження даних:
Всі дані зберігаються у папці користувача: ~/.assistant_data/
( через pickle)
Стан зберігається навіть при Ctrl+C.

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

Встановлення та запуск
Локальний запуск (із коду)
git clone <url-вашого-репозиторію>
cd goit-pycore-final
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt  # якщо є
python main.py                   # або: python main.py <шлях_до_файлу_контактів>


За замовчуванням контакти/нотатки зберігаються у ~/.assistant_data/.
Якщо передати шлях аргументом — збереження/завантаження відбуватиметься у цьому файлі.

Встановлення як пакет (опційно)
pip install -e .
assistant-bot   # якщо вказано console_scripts в проєкті

Команди (довідник)
Контакти
Команда	Опис	Приклад
hello	Привітання	hello
add [ім'я] [телефон]	Створити контакт або додати телефон до існуючого	add John 1234567890
change [ім'я] [старий телефон] [новий телефон]	Змінити телефон	change John 1234567890 0991112233
phone [ім'я]	Показати телефони контакту	phone John
all	Показати всі контакти	all
add-email [ім'я] [email]	Додати email у контакт	add-email John john@example.com
change-email [ім'я] [старий email] [новий email]	Змінити email	change-email John john@example.com john2@example.com
delete-email [ім'я] [email]	Видалити email	delete-email John john@example.com
show-email [ім'я]	Показати всі email-и контакту	show-email John
add-birthday [ім'я] [DD.MM.YYYY]	Додати ДН	add-birthday John 05.09.2000
show-birthday [ім'я]	Показати ДН	show-birthday John
birthdays [N]	Контакти, у кого ДН через N днів (без перенесення вихідних)	birthdays 7
search [запит]	Пошук контакту за ім'ям/телефоном/email (частковий збіг)	search joh

Примітки по валідації та унікальності:
Телефон — 10 цифр; глобально унікальний серед усіх контактів.
Email — глобально унікальний серед усіх контактів.
У межах одного контакту дублікати телефонів/email-адрес заборонені (чіткі помилки).

Службові
Команда	Опис
help або ?	Показати довідкову таблицю команд
close / exit	Зберегти дані та вийти
Ctrl+C	Акуратний вихід із збереженням стану

Приклади
Enter a command: add John 1234567890
Contact added.

Enter a command: add-email John john@example.com
Email added.

Enter a command: phone John
John: 1234567890

Enter a command: show-email John
john@example.com

Enter a command: add-birthday John 05.09.2000
Birthday added.

Enter a command: exit
Good bye!

Збереження даних
Формат — pickle. При відсутності файлів — створюються порожні.
При будь-якому виході (exit, close, Ctrl+C) виконується збереження стану.

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
