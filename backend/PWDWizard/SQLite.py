import sqlite3

def create_db():
    conn = sqlite3.connect('vault.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY,
            website TEXT NOT NULL,
            username TEXT NOT NULL,
            password BLOB NOT NULL
        )
    ''')
    conn.commit()
    conn.close()