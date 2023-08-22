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
              time TEXT,
              type_of_service TEXT,
              client_name TEXT,
              phone_number TEXT
              )
              ''')

    # Сохранить изменения
    conn.commit()


def add_client_name(name: str):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''INSERT INTO tatiana_working (client_name) VALUES (?)''', (name, ))
    conn.commit()


def add_phone_number(phone_number: int):
    id = _max_id()
    conn = get_connection()
    c = conn.cursor() 
    c.execute('''UPDATE tatiana_working SET phone_number = ? WHERE id = ?''', (phone_number, id))
    conn.commit()


def add_year(year: int):
    id = _max_id()
    conn = get_connection()
    c = conn.cursor()
    c.execute('''UPDATE tatiana_working SET year = ? WHERE id = ?''', (year, id))
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


def add_type_of_service(service):
    services = get_service()
    id = _max_id()
    conn = get_connection()
    c = conn.cursor()
    if services:
        c.execute('''UPDATE tatiana_working SET type_of_service = ? WHERE id = ?''', (''.join(services) + ',' +  service.capitalize(), id))
    else:
        c.execute('''UPDATE tatiana_working SET type_of_service = ? WHERE id = ?''', (service, id))
    conn.commit()



def get_client_name():
    id = _max_id()
    conn = get_connection()
    c = conn.cursor()
    c.execute('''SELECT client_name FROM tatiana_working WHERE id = ?''', (id, ))
    (res, ) = c.fetchone()
    return res


def get_phone_number():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''SELECT client_name, type_of_service, year, month, day, time FROM tatiana_working WHERE id = ?''', (id, ))
    (res, ) = c.fetchone()
    return res


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


def get_service():
    id = _max_id()
    conn = get_connection()
    c = conn.cursor()
    c.execute('''SELECT type_of_service FROM tatiana_working WHERE id = ?''', (id, ))
    (res, ) = c.fetchone()
    return res


def delete_last_record():
    id = _max_id()
    conn = get_connection()
    c = conn.cursor()
    c.execute('''DELETE FROM tatiana_working WHERE id = ?''', (id, ))
    conn.commit()


def delete_some_record(year, month, day, time):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''DELETE FROM tatiana_working 
              WHERE year = ? and month = ? and day = ? and time = ?''', (year, month, day, time))
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
        client_name, phone_number, year, month, day = get_client_name(), get_phone_number(), get_year(), get_month(), get_day()
        c.execute('''INSERT INTO tatiana_working (client_name, phone_number, year, month, day, time) 
                  VALUES (?, ?, ?, ?, ?, ?)''', (client_name, phone_number, year, month, day, time))
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


def get_all_records():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''SELECT client_name, phone_number, year, month, day, time, type_of_service FROM tatiana_working''')
    res = c.fetchall()
    return res


def get_some_records(phone_number):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''SELECT client_name, year, month, day, time, type_of_service FROM tatiana_working WHERE phone_number = ?''', (phone_number, ))
    res = c.fetchall()
    return res

if __name__ == '__main__': 
    init_db(force=True)
    print(get_some_records('+0682445335'))

