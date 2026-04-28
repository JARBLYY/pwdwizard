import mysql.connector
import os 


def get_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQLHOST", "db"),
        port=os.getenv("MYSQLPORT", 3306),
        user=os.getenv("MYSQLUSER", "root"),
        password=os.getenv("MYSQLPASSWORD", "password"),
        database=os.getenv("MYSQLDATABASE", "pwdwizard")
    )


def create_db():
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS passwords (
            id INT AUTO_INCREMENT PRIMARY KEY,
            website VARCHAR(255) NOT NULL,
            username VARCHAR(255) NOT NULL,
            password BLOB NOT NULL
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            id INT AUTO_INCREMENT PRIMARY KEY,
            salt BLOB NOT NULL
        )
    """)

    conn.commit()
    
    c.close()
    conn.close()


def load_or_create_salt():
    conn = get_connection()
    c = conn.cursor()

    c.execute("SELECT salt FROM settings LIMIT 1")
    result = c.fetchone()

    if result:
        salt = result[0]
    else:
        salt = os.urandom(16)  
        c.execute("INSERT INTO settings (salt) VALUES (%s)", (salt,))
        conn.commit()

    c.close()
    conn.close()
    return salt
