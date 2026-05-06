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
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) NOT NULL UNIQUE,
                password_hash VARCHAR(255) NOT NULL,
                salt BLOB NOT NULL
            )
        """)

        c.execute("""
            CREATE TABLE IF NOT EXISTS passwords (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                website VARCHAR(255) NOT NULL,
                username VARCHAR(255) NOT NULL,
                password BLOB NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)

        conn.commit()
        print("✓ Database and tables created successfully.")
        c.close()
        conn.close()
    except Exception as e:
        print(f"✗ Database connection failed: {str(e)}")


def create_user(username, password_hash, salt):
    """Create a new user. Returns user_id, or None if username taken."""
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute(
            "INSERT INTO users (username, password_hash, salt) VALUES (%s, %s, %s)",
            (username, password_hash, salt)
        )
        conn.commit()
        user_id = c.lastrowid
        return user_id
    except mysql.connector.IntegrityError:
        return None
    finally:
        c.close()
        conn.close()


def get_user(username):
    """Get user by username. Returns (id, password_hash, salt) or None."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id, password_hash, salt FROM users WHERE username = %s", (username,))
    result = c.fetchone()
    c.close()
    conn.close()
    return result