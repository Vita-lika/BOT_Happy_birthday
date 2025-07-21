import sqlite3
from loguru import logger


class BirthdayDatabase:
    def __init__(self, db_name: str = "birthdays.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_database()

    def create_database(self):
        with self.conn:
            self.conn.execute('''
            CREATE TABLE IF NOT EXISTS birthdays (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                birth_date TEXT NOT NULL,
                group_name TEXT NOT NULL
            )
            ''')

    def add_birthday(self, full_name: str, birth_date: str, group_name: str):
        with self.conn:
            self.conn.execute(
                "INSERT INTO birthdays (full_name, birth_date,\
                    group_name) VALUES (?, ?, ?)",
                (full_name, birth_date, group_name)
            )

    def get_birthdays_by_group(self, group_name: str):
        with self.conn:
            cursor = self.conn.execute(
                "SELECT full_name, birth_date \
                    FROM birthdays WHERE group_name = ? ORDER BY full_name",
                (group_name,)
            )
            return cursor.fetchall()

    def print_all_birthdays(self):
        rpo_birthdays = self.get_birthdays_by_group('РПО')
        gd_birthdays = self.get_birthdays_by_group('ГД')

        print("РПО:")
        for i, (name, date) in enumerate(rpo_birthdays, 1):
            print(f"{i}.\t{name} – {date}")

        print("\nГД:")
        for i, (name, date) in enumerate(gd_birthdays, 1):
            print(f"{i}.\t{name} – {date}")

    def delete_birthday(self, record_id: int):
        with self.conn:
            self.conn.execute("DELETE FROM birthdays\
                WHERE id = ?", (record_id,))

    def initialize_sample_data(self):

        sample_data = [
            # РПО
            ("Гюнашян Владислав Самвелович", "20.06.2008", "РПО"),
            ("Маклюсов Кирилл Михайлович", "17.06.2009", "РПО"),
            ("Манираки Александр Александрович", "10.10.2009", "РПО"),
            ("Мокряков Илья Александрович", "20.03.2008", "РПО"),
            ("Николаев Вадим Евгеньевич", "14.07.2008", "РПО"),
            ("Попов Георгий Андреевич", "28.04.2007", "РПО"),
            ("Симончук Асинья Игоревна", "11.12.2007", "РПО"),
            ("Соломахин Владислав Павлович", "22.06.2009", "РПО"),
            ("Солонченко Кирилл Романович", "04.10.2008", "РПО"),
            ("Степанов Арсений Дмитриевич", "06.09.2006", "РПО"),
            ("Ткаченко Виталина Романовна", "12.10.2008", "РПО"),
            ("Фетисов Тимур Николаевич", "20.06.2008", "РПО"),

            # ГД
            ("Болкарева Анна Петровна", "22.06.2008", "ГД"),
            ("Коржавчиков Георгий Викторович", "26.01.2003", "ГД"),
            ("Мордвинкова Вероника Ильинична", "22.04.2006", "ГД"),
            ("Мыктыбеков Аят Эдилович", "29.08.2009", "ГД"),
            ("Подлесных Татьяна Андреевна", "21.01.2008", "ГД"),
            ("Соловьева Виктория Александровна", "02.07.2006", "ГД"),
            ("Шарапатов Андрей Павлович", "02.11.2007", "ГД"),
            ("Шелковский Дмитрий Денисович", "09.10.2008", "ГД")
        ]

        with self.conn:
            self.conn.execute("DELETE FROM birthdays")
            self.conn.executemany(
                "INSERT INTO birthdays (full_name, birth_date,\
                    group_name) VALUES (?, ?, ?)",
                sample_data
            )


db = BirthdayDatabase()
db.initialize_sample_data()
db.print_all_birthdays()
