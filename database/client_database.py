import sqlite3

__connection = None

def get_connection():
    global __connection
    if __connection is None:
        __connection = sqlite3.connect('tatiana_working.db')
    return __connection



class GetConnection:

    def __init__(self):
        self.conn = get_connection()
        self.c = self.conn.cursor()


class InitDatabase(GetConnection):

    # Метод инициализации базы данных
    def init_db(self, force: bool = False):
        # Проверить что нужные таблицы существуют, иначе создать их
        # force - явно пересоздать все таблицы
        # Сообщения от пользователя
        if force:
            self.c.execute("DROP TABLE IF EXISTS clients") 

        self.c.execute('''CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_name TEXT,
                type_of_service TEXT,
                date DATETIME,
                phone_number TEXT,
                user_id INTEGER
        )''')
        # Сохранить изменения
        self.conn.commit()


class Records(GetConnection):

    def __init__(self, client_name=None, type_of_service=None, date=None, phone_number=None, user_id=None):
        super().__init__()
        self.client_name = client_name
        self.type_of_services = type_of_service
        self.date = date
        self.phone_number = phone_number
        self.user_id = user_id


class AddRecord(Records):

    def add_record(self):
        self.c.execute('''INSERT INTO clients (client_name, type_of_service, date, phone_number, user_id)
                       VALUES (?, ?, ?, ?, ?)''', (self.client_name, self.type_of_services, self.date, self.phone_number, self.user_id))
        self.conn.commit()


class CountRecords(Records):

    def count_records(self):
        self.c.execute('''SELECT COUNT(*) FROM clients 
                       WHERE client_name = ? and type_of_service = ? and date = ? and phone_number = ? and user_id = ?
                       ''', (self.client_name, self.type_of_services, self.date, self.phone_number, self.user_id))
        (res, ) = self.c.fetchone()
        return res


class GetRecords(Records):

    def get_records(self):
        self.c.execute('''SELECT type_of_service, date 
                       FROM clients WHERE user_id = ?''', (self.user_id, ))
        res = self.c.fetchall()
        return res


if __name__ == '__main__':
    records = CountRecords('Kirill', 'Брови', '2023.12.23.17:00', '0682445335', '518571').count_records()
