from PWDWizard.EncryptAndDecrypt import encrypt_password, decrypt_password
from PWDWizard.generator import generate_password
import sqlite3

def save_password(website, username, password, key):
    encrypted = encrypt_password(key, password)

    conn = sqlite3.connect("vault.db")
    c = conn.cursor()

    c.execute(
        "INSERT INTO passwords (website, username, password) VALUES (?, ?, ?)",
        (website, username, encrypted)
    )

    conn.commit()
    conn.close()

def save_generated_password(website, username, key):
    password = generate_password(12)
    save_password(website, username, password, key)
    return password

def get_passwords(key):
    conn = sqlite3.connect("vault.db")
    c = conn.cursor()

    c.execute("SELECT website, username, password FROM passwords")
    rows = c.fetchall()

    if not rows:
        print("No passwords saved yet.")
    else:
        for website, username, encrypted_pw in rows:
            decrypted_pw = decrypt_password(key, encrypted_pw)
            print(f"Website: {website} | Username: {username} | Password: {decrypted_pw}")

    conn.close()