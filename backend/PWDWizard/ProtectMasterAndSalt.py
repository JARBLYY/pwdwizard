import os


def load_or_create_salt():
    if not os.path.exists('salt.bin'):
        salt = os.urandom(16)
        with open('salt.bin', 'wb') as f:
            f.write(salt)
    else:
        with open('salt.bin', 'rb') as f:
            salt = f.read()
    return salt