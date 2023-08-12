import sqlite3


__connection = None

def get_connection():
    global __connection
    if __connection is None:
        __connection = sqlite3.connect('tatiana_working.db')
    return __connection


def init_db(force: bool = False):
    # Проверить что нужные таблицы существуют, иначе создать их
    # force - явно пересоздать все таблицы
    conn = get_connection()
    c = conn.cursor()

    # Сообщения от пользователя
    if force:
        c.execute('DROP TABLE IF EXISTS tatiana_working')

    c.execute('''
              CREATE TABLE IF NOT EXISTS tatiana_working (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              year INTEGER,
              month INTEGER,
              days TEXT,
              time TEXT
              )
              ''')

    # Сохранить изменения
    conn.commit()


def add_year_start(year: int):
    if _check_year(year):
        conn = get_connection()
        c = conn.cursor()
        c.execute('''INSERT INTO tatiana_working (year) VALUES (?)''', (year, ))
        conn.commit()


def _check_year(year: int):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''SELECT COUNT(*) FROM tatiana_working WHERE year = ?''', (year, ))
    (num, ) = c.fetchone()
    if num <= 12:
        return True
    return False


def add_month_start(year: int, month: int):
    if _check_month(year, month):
        conn = get_connection()
        c = conn.cursor()
        c.execute('''UPDATE tatiana_working SET month = ? WHERE month is NULL''', (month, ))
        conn.commit()


def _check_month(year: int, month: int):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''SELECT COUNT(*) FROM tatiana_working WHERE month = ? and year = ?''', (month, year))
    (count, ) = c.fetchone()
    if not count:
        return True
    return False


def get_year():
    conn = get_connection()
    c = conn.cursor() 
    c.execute('''SELECT MAX(year) FROM tatiana_working''')
    (res, ) = c.fetchone()
    return res



if __name__ == '__main__':
    init_db(force=True)
    add_year_start(2023)
    add_month_start(1)
    add_year_start(2024)
    add_month_start(1)
    add_year_start(2023)
    add_month_start(1)
    get_year()
