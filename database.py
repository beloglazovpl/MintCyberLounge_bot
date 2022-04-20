import sqlite3


class BotDB:

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def create_table_users(self):
        """Создаем таблицу пользователей"""
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER PRIMARY KEY,
            user_name TEXT,
            user_surname TEXT,
            username TEXT);
            """
        )
        return self.conn.commit()

    def create_table_records(self):
        """Создаем таблицу записей"""
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS records(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL REFERENCES users(user_id),
            date_time_add TIMESTAMP,
            method TEXT,
            data TEXT,
            event TEXT);
            """
        )
        return self.conn.commit()

    def user_exists(self, user_id):
        """Проверяем, есть ли юзер в базе"""
        result = self.cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
        return bool(len(result.fetchall()))

    def get_user_id(self, user_id):
        """Достаем id юзера в базе по его user_id"""
        result = self.cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
        return result.fetchone()[0]

    def add_user(self, user_id, user_name, user_surname, username):
        """Добавляем юзера в базу"""
        self.cursor.execute('INSERT INTO users (user_id, user_name, user_surname, username) VALUES (?, ?, ?, ?)',
                   (user_id, user_name, user_surname, username))
        return self.conn.commit()

    def add_data(self, user_id, date_time_add, method, data, event):
        """Создаем запись ответа пользователя"""
        self.cursor.execute('INSERT INTO records (user_id, date_time_add, method, data, event) VALUES (?, ?, ?, ?, ?)',
                   (user_id, date_time_add, method, data, event))
        return self.conn.commit()

    def close(self):
        """Закрываем соединение с БД"""
        self.conn.close()
