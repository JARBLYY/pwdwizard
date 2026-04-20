from cryptography.fernet import Fernet

def encrypt_password(key, password):
    fernet = Fernet(key)
    return fernet.encrypt(password.encode())

def decrypt_password(key, token):
    fernet = Fernet(key)
    return fernet.decrypt(token).decode()