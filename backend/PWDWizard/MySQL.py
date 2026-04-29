import mysql.connector
import os


def get_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQLHOST"),
        port=int(os.getenv("MYSQLPORT", 3306)),
        user=os.getenv("MYSQLUSER", "root"),
        password=os.getenv("MYSQL_ROOT_PASSWORD"),
        database=os.getenv("MYSQLDATABASE", "railway")
    )


def create_db():
    try:
        conn = get_connection()
        print(f"✓ Connected to MySQL at {os.getenv('MYSQLHOST')}")
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
        print("✓ Database and tables created successfully.")
        c.close()
        conn.close()
    except Exception as e:
        print(f"✗ Database connection failed: {str(e)}")


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