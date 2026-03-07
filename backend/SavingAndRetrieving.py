
from PWDWizard.EncryptAndDecrypt import encrypt_password, decrypt_password
import mysql.connector

def save_password(website, username, password, key):
    encrypted = encrypt_password(key, password)

    conn = mysql.connector.connect(
        host="db",
        user="root",
        password="password",
        database="pwdwizard"
    )
    c = conn.cursor()

    c.execute(
        "INSERT INTO passwords (website, username, password) VALUES (%s, %s, %s)",
        (website, username, encrypted)
    )

    conn.commit()
    conn.close()

def get_passwords(key):
    conn = mysql.connector.connect(
        host="db",
        user="root",
        password="password",
        database="pwdwizard"
    )
    c = conn.cursor()

    c.execute("SELECT website, username, password FROM passwords")

    for row in c.fetchall():
        website, username, encrypted_pw = row
        decrypted_pw = decrypt_password(key, encrypted_pw)
        print(f"Website: {website} | Username: {username} | Password: {decrypted_pw}")

    conn.close()