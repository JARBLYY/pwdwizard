from PWDWizard.MasterPassword import get_key_from_password
from PWDWizard.ProtectMasterAndSalt import load_or_create_salt
from PWDWizard.SQLite import create_db
from PWDWizard.SavingAndRetrieving import save_password, get_passwords

def main():
    salt = load_or_create_salt()
    master_pw = input("Enter your master password: ")
    key = get_key_from_password(master_pw, salt)

    while True:
        print("\n1. Save Password")
        print("2. View Passwords")
        print("3. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            site = input("Website: ")
            user = input("Username: ")
            pw = input("Password: ")
            save_password(site, user, pw, key)

        elif choice == "2":
            get_passwords(key)

        elif choice == "3":
            break

if __name__ == "__main__":
    create_db()
    main()