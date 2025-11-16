from datetime import datetime
from birthday import Birthday
from address_book import AddressBook

BIRTHDAY_REMINDER = 7
MINIMUM_COLUMN_WIDTH = 16
BIRTHDAY_COLUMN_WIDTH = 12

def get_upcoming_birthdays(book : AddressBook):

    #Повертає список контактів, у яких день народження відбудеться
    #протягом наступних BIRTHDAY_REMINDER днів.
    
        today = datetime.today().date()
        upcoming_birthdays = []

        for name, record in book.data.items():
            if record.birthday:

                birth_dt = record.birthday.value.date()
                birthday = birth_dt.replace(year=today.year)

                # Якщо в цьому році ДР вже минув — беремо наступний рік
                if birthday < today:
                    birthday = birthday.replace(year=today.year + 1)

                delta = (birthday - today).days

                if 0 <= delta <= BIRTHDAY_REMINDER:
                    upcoming_birthdays.append(
                        {
                            "name": name,
                            "birthday_date": birthday.strftime(Birthday.DATE_FORMAT),
                        }
                    )

        return upcoming_birthdays


def show_upcoming_birthdays(book : AddressBook) -> None:
    # ======= кольоровий вивід + подвійна рамка + emoji 🎉 =======

    # ANSI кольори
    YELLOW = "\033[33m"
    GREEN = "\033[32m"
    CYAN = "\033[36m"
    RESET = "\033[0m"

    upcoming = get_upcoming_birthdays(book)

    if upcoming:

        #pick right name column width
        names_max_width = max(len(col['name'])  for col in upcoming)
        if names_max_width < MINIMUM_COLUMN_WIDTH :
             names_max_width = MINIMUM_COLUMN_WIDTH
        print(names_max_width)

        print(f"\n{YELLOW}🎉 Upcoming birthdays within the next 7 days 🎉{RESET}\n")

        # Подвійні лінії для таблиці
        top_line    = "╔" + "═" * names_max_width + "╦" + "═" * BIRTHDAY_COLUMN_WIDTH + "╗"
        header_line = "║ {name:<{nwidth}}║ {bdate:<{bwidth}}║".format(
             name = "Name", 
             bdate = "Birthday", 
             nwidth = names_max_width-1, 
             bwidth = BIRTHDAY_COLUMN_WIDTH -1
             )
        mid_line    = "╠" + "═" * names_max_width+ "╬" + "═" * BIRTHDAY_COLUMN_WIDTH + "╣"
        bottom_line = "╚" + "═" * names_max_width + "╩" + "═" * BIRTHDAY_COLUMN_WIDTH + "╝"

        # Друк таблиці
        print(CYAN + top_line + RESET)
        print(CYAN + header_line + RESET)
        print(CYAN + mid_line + RESET)

        for item in upcoming:
            name = item['name']
            date = item['birthday_date']
            row = f"{CYAN}║ {GREEN}{name:<{names_max_width-1}}{CYAN}║ {GREEN}{date:<{BIRTHDAY_COLUMN_WIDTH-1}}{CYAN}║"
            print(row)

        print(CYAN + bottom_line + RESET + "\n")