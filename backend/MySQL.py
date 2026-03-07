import mysql.connector

def create_db():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password"
    )

    c = conn.cursor()

    c.execute("CREATE DATABASE IF NOT EXISTS pwdwizard")
    c.execute("USE pwdwizard")

    c.execute("""
        CREATE TABLE IF NOT EXISTS passwords (
            id INT AUTO_INCREMENT PRIMARY KEY,
            website VARCHAR(255) NOT NULL,
            username VARCHAR(255) NOT NULL,
            password BLOB NOT NULL
        )
    """)

    conn.commit()
    conn.close()