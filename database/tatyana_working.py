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
              'Имя мастера' TEXT NOT NULL,
              'Месяц начало работы' DATETIME NOT NULL,
              'Год начало работы' DATETIME NOT NULL
    )''')

    # Сохранить изменения
    conn.commit()


def add_messages(master_name, year_when_start_working, month_when_start_working):
    if _check_month_and_day(master_name, year_when_start_working, month_when_start_working):
        conn = get_connection()
        c = conn.cursor()
        c.execute('''INSERT INTO tatyana_working 
                  ('Имя мастера', 'Год начало работы', 'Месяц начало работы') 
                  VALUES (?, ?, ?)''', 
                  (master_name, year_when_start_working, month_when_start_working))
        conn.commit()


def _check_month_and_day(master, year, month):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
              SELECT 'Имя мастера', 'Год начало работы', 'Месяц начало работы' 
              FROM tatyana_working 
              WHERE 'Имя мастера'=? and 'Год начало работы'=? and 'Месяц начало работы'=? 
              LIMIT 3''', (master, year, month))
    if not len(c.fetchall()):
        return True
    return False


#if __name__ == '__main__':
 #   init_db(force=True)