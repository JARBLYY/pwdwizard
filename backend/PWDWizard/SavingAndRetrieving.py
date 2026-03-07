from PWDWizard.EncryptAndDecrypt import encrypt_password, decrypt_password
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

def get_passwords(key):
    conn = sqlite3.connect("vault.db")
    c = conn.cursor()

    c.execute("SELECT website, username, password FROM passwords")

    for website, username, encrypted_pw in c.fetchall():
        decrypted_pw = decrypt_password(key, encrypted_pw)
        print(f"Website: {website} | Username: {username} | Password: {decrypted_pw}")

    conn.close()