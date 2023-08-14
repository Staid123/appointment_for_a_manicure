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
              day INTEGER,
              time TEXT
              )
              ''')

    # Сохранить изменения
    conn.commit()


# Добавить год в базу данных
def add_year(year: int):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''INSERT INTO tatiana_working (year) VALUES (?)''', (year, ))
    conn.commit()


def add_month(month: int):
    id = _max_id()
    conn = get_connection()
    c = conn.cursor()
    c.execute('''UPDATE tatiana_working SET month = ? WHERE id = ?''', (month, id))
    conn.commit()


def add_day(day: int):
    id = _max_id()
    conn = get_connection()
    c = conn.cursor()
    c.execute('''UPDATE tatiana_working SET day = ? WHERE id = ?''', (day, id))
    conn.commit()


def add_time(time: str):
    id = _max_id()
    conn = get_connection()
    c = conn.cursor()
    c.execute('''UPDATE tatiana_working SET time = ? WHERE id = ?''', (time, id))
    conn.commit()


def get_year():
    id = _max_id()
    conn = get_connection()
    c = conn.cursor() 
    c.execute('''SELECT year FROM tatiana_working WHERE id = ?''', (id, ))
    (res, ) = c.fetchone()
    return res


def get_month():
    id = _max_id()
    conn = get_connection()
    c = conn.cursor()
    c.execute('''SELECT month FROM tatiana_working WHERE id = ?''', (id, ))
    (res, ) = c.fetchone()
    return res


def get_day():
    id = _max_id()
    conn = get_connection()
    c = conn.cursor()
    c.execute('''SELECT day FROM tatiana_working WHERE id = ?''', (id, ))
    (res, ) = c.fetchone()
    return res


def delete_record():
    id = _max_id()
    conn = get_connection()
    c = conn.cursor()
    c.execute('''DELETE FROM tatiana_working WHERE id = ?''', (id, ))
    conn.commit()


def _max_id():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''SELECT MAX(id) FROM tatiana_working''')
    (res, ) = c.fetchone()
    return res


def _check_time():
    id = _max_id()
    conn = get_connection()
    c = conn.cursor()
    c.execute('''SELECT time FROM tatiana_working WHERE id = ?''', (id, ))
    (res, ) = c.fetchone()
    return res


def insert_new_record(time: str):
    conn = get_connection()
    c = conn.cursor()
    is_time = _check_time()
    if is_time:
        year, month, day = get_year(), get_month(), get_day()
        c.execute('''INSERT INTO tatiana_working (year, month, day, time) VALUES (?, ?, ?, ?)''', (year, month, day, time))
    else:
        add_time(time)
    conn.commit()


def how_many_time():
    conn = get_connection()
    c = conn.cursor()
    year, month, day = get_year(), get_month(), get_day()
    c.execute('''SELECT time FROM tatiana_working WHERE year = ? and month = ? and day = ?''', (year, month, day))
    res = c.fetchall()
    return res


if __name__ == '__main__':
    init_db()
    print(how_many_time())

