import sqlite3
from sqlite3 import Error

DATABASE = 'app/vkinder.db'

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect(DATABASE)
        create_table(conn)  # Вызываем функцию create_table после установки соединения
    except Error as e:
        print(e)

    if conn:
        return conn

def create_table(conn):
    try:
        query = '''CREATE TABLE IF NOT EXISTS Users (
                        id integer PRIMARY KEY,
                        first_name text NOT NULL,
                        last_name text NOT NULL,
                        profile_link text NOT NULL,
                        photos text NOT NULL
                   );'''

        conn.execute(query)
    except Error as e:
        print(e)

def add_user(conn, user):
    """
    Добавляет пользователя в базу данных.
    Возвращает ID добавленного пользователя.
    """
    sql = ''' INSERT INTO Users(id, first_name, last_name, profile_link, photos)
              VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, user)
    conn.commit()
    return cur.lastrowid

def user_exists(conn, user_id):
    """
    Проверяет, существует ли пользователь в базе данных.
    Возвращает True, если пользователь существует, иначе - False.
    """
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM Users WHERE id=?", (user_id,))

    return cur.fetchone() is not None
