import sqlite3

__connection = None

def get_connection():
    global __connection
    if __connection is None:
        __connection = sqlite3.connect('manicure1.db')
    return __connection


def init_db(force: bool = False):
    # Проверить что нужные таблицы существуют, иначе создать их
    # force - явно пересоздать все таблицы
    conn = get_connection()
    c = conn.cursor()

    # Сообщения от пользователя
    if force:
        c.execute("DROP TABLE IF EXISTS manicure1")
    
    c.execute('''CREATE TABLE IF NOT EXISTS manicure1 (
              id INTEGER PRIMARY KEY,
              user_id INTEGER NOT NULL,
              status TEXT NOT NULL
    )''')

    # Сохранить изменения
    conn.commit()


def add_messages(user_id: int, status: str):
    if not count_messages(user_id):
        conn = get_connection()
        c = conn.cursor()
        c.execute('''INSERT INTO manicure1 (user_id, status) VALUES (?, ?)''', (user_id, status))
        conn.commit()


def count_messages(user_id: int):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''SELECT COUNT(*) FROM manicure1 WHERE user_id = ?''', (user_id, ))
    (res, ) = c.fetchone()
    return res



if __name__ == '__main__':
    init_db(force=True)
    add_messages(12355, 'user')
    add_messages(12355, 'user')
    print(count_messages(12355))