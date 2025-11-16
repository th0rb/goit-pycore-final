from error import input_error
from address_book import AddressBook
from record import Record
from string import ascii_uppercase
from colorama import init, Fore, Style


init(autoreset=True)

TITLE = Fore.MAGENTA + Style.BRIGHT
LABEL = Fore.CYAN
VAL = Fore.GREEN + Style.BRIGHT
WARNING = Fore.YELLOW
ERROR = Fore.RED + Style.BRIGHT
RESET = Style.RESET_ALL

ALPHA_EMOJI = {
    c: chr(0x1F150 + i)  # 🅐 🅑 🅒 ...
    for i, c in enumerate(ascii_uppercase)
}

not_found_message = "Contact does not exist, you can add it"

def pad_lines(lines, width):
    """Додає пробіли справа, щоб всі рядки були однакової довжини."""
    return [line + " " * (width - len(line)) for line in lines]

@input_error
def add_contact(book: AddressBook, *args):
    name, phone = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        if book.is_phone_taken(phone):
            return "Цей номер уже використовується іншим контактом."
        record.add_phone(phone)
    return message


@input_error
def change_phone(book: AddressBook, *args):
    if len(args) != 3:
        return 'Invalid number of arguments. Usage: change [name] [old_number] [new_number]'
    name, old_number, new_number = args
    record = book.find(name)
    if record is None:
        return not_found_message
    if old_number == new_number:
        return "Змін немає (старий і новий номер однакові)."
    if book.is_phone_taken(new_number):
        return "Цей номер уже використовується іншим контактом."
    record.edit_phone(old_number, new_number)
    return "Номер змінено."


@input_error
def show_phone(book: AddressBook, *args):
    if len(args) != 1:
        return ERROR + "Usage: show-phone [name]"

    name = args[0]
    record = book.find(name)

    if record is None:
        return ERROR + not_found_message

    phones = [f"📞 {p.value}" for p in record.phones] or ["No phones"]
    width = max(len(x) for x in phones)

    phones = pad_lines(phones, width)

    top = f"{TITLE}╔════════════════════╦═{'═'*width}╗"
    header = f"{TITLE}║ Name               ║ Phones{' '*(width-6)}║"
    mid = f"{TITLE}╠════════════════════╬═{'═'*width}╣"
    bottom = f"{TITLE}╚════════════════════╩═{'═'*width}╝"

    rows = [
        top,
        header,
        mid,
        *[f"║ {VAL}{name:<18}{RESET} ║ {VAL}{line}{RESET} ║" for line in phones],
        bottom
    ]

    return "\n".join(rows)



@input_error
def show_all_contacts(book: AddressBook):
    if len(book) == 0:
        return WARNING + "Address book is empty."

    contacts = list(book.values())

    # Сортуємо по алфавіту
    contacts.sort(key=lambda r: r.name.value.lower())

    # Групуємо
    groups = {}
    for rec in contacts:
        first = rec.name.value[0].upper()
        if not first.isalpha():
            first = "#"
        groups.setdefault(first, []).append(rec)

    output = []

    # Перебір груп у алфавітному порядку
    for letter in sorted(groups.keys()):
        group = groups[letter]

        emoji = ALPHA_EMOJI.get(letter, "🔤")

        output.append(f"\n{TITLE}{emoji}  {letter}{RESET}")

        # Готуємо таблицю групи
        table_data = []
        for rec in group:
            phones = [f"📞 {p.value}" for p in rec.phones] or [""]
            emails = [f"✉️ {e.value}" for e in rec.emails] or [""]
            birthday = f"📅 {rec.birthday.value.strftime('%d.%m.%Y')}" if rec.birthday else ""

            max_h = max(len(phones), len(emails))
            phones += [""] * (max_h - len(phones))
            emails += [""] * (max_h - len(emails))

            table_data.append({
                "name": rec.get_print_name(),
                "phones": phones,
                "emails": emails,
                "birthday": birthday
            })

        # Ширини
        w_name  = max(len(t["name"])  for t in table_data) + 2
        w_phone = max(len(x) for t in table_data for x in t["phones"]) + 2
        if w_phone < 8: w_phone = 8 #min width
        w_email = max(len(x) for t in table_data for x in t["emails"]) + 2
        if w_email < 8: w_email = 8 #min width
        w_birth = max(len(t["birthday"]) for t in table_data) + 2
        if w_birth < 10: w_birth = 10 #min width

        top     = f"{TITLE}╔═{'═'*w_name}═╦═{'═'*w_phone}═╦═{'═'*w_email}═╦═{'═'*w_birth}═╗"
        header  = f"║ Name{' '*(w_name-4)} ║ Phones{' '*(w_phone-6)} ║ Emails{' '*(w_email-6)} ║ Birthday{' '*(w_birth-8)} ║"
        sep     = f"╠═{'═'*w_name}═╬═{'═'*w_phone}═╬═{'═'*w_email}═╬═{'═'*w_birth}═╣"
        mid_sep = f"╠═{'═'*w_name}═╬═{'═'*w_phone}═╬═{'═'*w_email}═╬═{'═'*w_birth}═╣"
        bottom  = f"╚═{'═'*w_name}═╩═{'═'*w_phone}═╩═{'═'*w_email}═╩═{'═'*w_birth}═╝"

        output.append(top)
        output.append(header)
        output.append(sep)

        for entry in table_data:
            name = entry["name"]
            phones = entry["phones"]
            emails = entry["emails"]
            birthday = entry["birthday"]
            if not birthday : birthday = " " * (w_birth + 1)

            for i in range(max(len(phones), len(emails))):
                output.append(
                    RESET + "║ " 
                    + (VAL + f"{name:<{w_name}} " + RESET if i == 0 else " " * (w_name + 1))
                    + f"║ {VAL}{phones[i]:<{w_phone}}{RESET}"
                    + "║ " 
                    + (VAL + f"{emails[i]:<{w_email+1}} " + RESET if emails[i] else " " * (w_email + 1))
                    + "║ " 
                    + (VAL + f"{birthday:<{w_birth}}" + RESET if i == 0 else " " * (w_birth + 1)) + "║"
                )
            output.append(mid_sep)

        # Замінюємо останній роздільник на низ таблиці
        output[-1] = bottom

    return "\n".join(output)


def draw_table(data) -> str:
    pass


@input_error
def search(book: AddressBook, *args):
    if not args:
        return "Invalid number of arguments. Usage: search [text]"
    
    # Підтримуємо пошук за кількома словами: search John Doe
    query = " ".join(args).lower()

    # Визначаємо, чи запит схожий на email
    is_email_query = False
    if " " not in query and "@" in query:
        local_part, _, domain_part = query.partition("@")
        if local_part and "." in domain_part:
            is_email_query = True

    matches = []
    for record in book.values():
        # ----- ПОШУК ПО ІМЕНІ (завжди) -----
        if query in record.name.value.lower():
            matches.append(record.name.value)
            continue

        if is_email_query:
            # ----- ЗАПИТ СХОЖИЙ НА EMAIL → ШУКАЄМО ПО EMAIL -----
            emails = getattr(record, "emails", [])
            for email in emails:
                if query in email.value.lower():
                    matches.append(record.name.value)
                    break
        else:
            # ----- НЕ EMAIL → ШУКАЄМО ПО ТЕЛЕФОНУ -----
            phones = getattr(record, "phones", [])
            for phone in phones:
                if query in phone.value:
                    matches.append(record.name.value)
                    break

    if not matches:
        return "No contacts found for this query."

    # Формуємо нормальний вивід
    result = []
    for record in book.values():
        if record.name.value in matches:
            result.append(str(record))

    return "\n".join(result)

@input_error
def add_email(book: AddressBook, *args):
    name, email = args
    record = book.find(name)
    if record is None:
        record = Record(name)
        book.add_record(record)
    if book.is_email_taken(email):
        return "Цей email уже використовується іншим контактом."
    record.add_email(email)
    return "Email додано."

@input_error
def change_email(book: AddressBook, *args):
    name, old_e, new_e = args
    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found")
    if old_e == new_e:
        return "Змін немає (старий і новий email однакові)."
    if book.is_email_taken(new_e):
        return "Цей email уже використовується іншим контактом."
    record.edit_email(old_e, new_e)
    return "Email оновлено."

@input_error
def delete_email(book: AddressBook, *args):
    name, e = args
    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found")
    record.remove_email(e)
    return "Email видалено."

@input_error
def show_email(book: AddressBook, *args):
    name, = args
    record = book.find(name)

    if record is None:
        return ERROR + "Contact not found"

    emails = [f"✉️ {e.value}" for e in record.emails] or ["No emails"]
    width = max(len(x) for x in emails)
    emails = pad_lines(emails, width)

    top = f"{TITLE}╔════════════════════╦═{'═'*width}╗"
    header = f"{TITLE}║ Name               ║ Emails{' '*(width-6)}║"
    mid = f"{TITLE}╠════════════════════╬═{'═'*width}╣"
    bottom = f"{TITLE}╚════════════════════╩═{'═'*width}╝"

    rows = [
        top,
        header,
        mid,
        *[f"║ {VAL}{name:<18}{RESET} ║ {VAL}{line}{RESET} ║" for line in emails],
        bottom
    ]

    return "\n".join(rows)


@input_error
def add_birthday(book: AddressBook, *args):
    if len(args) != 2:
        return "Invalid number of arguments. Usage: add-birthday [name] [date]"
    name, date = args
    record = book.find(name)
    if record:
        record.add_birthday(date)
        return "Birthday added."
    else:
        return not_found_message
    
@input_error
def show_birthday(book: AddressBook, *args):
    if len(args) != 1:
        return "Invalid number of arguments. Usage: show-birthday [name]"
    name = args[0]
    record = book.find(name)
    if record:
        if record.birthday:
            return record.birthday
        else:
            return "Birthday not added to this contact."
    else:
        return not_found_message