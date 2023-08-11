import sqlite3

__connection = None

def get_connection():
    global __connection
    if __connection is None:
        __connection = sqlite3.connect('tatyana_working.db')
    return __connection


def init_db(force: bool = False):
    # Проверить что нужные таблицы существуют, иначе создать их
    # force - явно пересоздать все таблицы
    conn = get_connection()
    c = conn.cursor()

    # Сообщения от пользователя
    if force:
        c.execute('''DROP TABLE IF EXISTS tatyana_working''')

    c.execute('''CREATE TABLE IF NOT EXISTS tatyana_working (
              month TEXT NOT NULL,
              day INTEGER NOT NULL
    )''')

    # Сохранить изменения
    conn.commit()


def add_messages(month, day):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''INSERT INTO tatyana_working (month, day) VALUES (?, ?)''', (month, day))
    conn.commit()

def _check_month_and_day(month, day):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''SELECT month, day FROM tatyana_working WHERE month=? and day=? LIMIT 2''', (month, day))
    if not len(c.fetchall()):
        return True
    return False

if __name__ == '__main__':
    init_db(force=True)
    add_messages('March', 20)
    print(_check_month_and_day('March', 20))