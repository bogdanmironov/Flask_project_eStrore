import sqlite3 as sqlite

DB_NAME = "eStore.db"

conn = sqlite.connect(DB_NAME)

conn.cursor().execute('''
CREATE TABLE IF NOT EXISTS user
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT,
        username TEXT,
        password TEXT,
        address TEXT,
        phone TEXT
    )''')

conn.commit()

conn.cursor().execute('''
CREATE TABLE IF NOT EXISTS advert
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        description TEXT,
        price REAL,
        creation_date TEXT,
        is_active INTEGER,
        buyer_id TEXT,
        user_id INTEGER
    )''')

conn.commit()

class SQLite(object):

    def __enter__(self):
        self.conn = sqlite.connect(DB_NAME)
        return self.conn.cursor()

    def __exit__(self, type, value, traceback):
        self.conn.commit()
        