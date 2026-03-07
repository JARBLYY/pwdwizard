import sqlite3

def create_db():
    conn = sqlite3.connect("vault.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS passwords (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        website TEXT,
        username TEXT,
        password BLOB
    )
    """)

    conn.commit()
    conn.close()