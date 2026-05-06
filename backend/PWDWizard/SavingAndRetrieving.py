from PWDWizard.EncryptAndDecrypt import encrypt_password, decrypt_password
from PWDWizard.generator import generate_password
from PWDWizard.MySQL import get_connection


def save_password(website, username, password, key, user_id):
    encrypted = encrypt_password(key, password)

    conn = get_connection()
    c = conn.cursor()

    c.execute(
        "INSERT INTO passwords (user_id, website, username, password) VALUES (%s, %s, %s, %s)",
        (user_id, website, username, encrypted)
    )

    conn.commit()
    c.close()
    conn.close()


def save_generated_password(website, username, key, user_id):
    password = generate_password(12)
    save_password(website, username, password, key, user_id)
    return password


def get_passwords(key, user_id):
    conn = get_connection()
    c = conn.cursor()

    c.execute(
        "SELECT website, username, password FROM passwords WHERE user_id = %s",
        (user_id,)
    )
    rows = c.fetchall()

    c.close()
    conn.close()

    results = []
    for website, username, encrypted_pw in rows:
        try:
            decrypted_pw = decrypt_password(key, encrypted_pw)
        except Exception:
            decrypted_pw = "[decryption failed]"
        results.append({"website": website, "username": username, "password": decrypted_pw})
    return results
