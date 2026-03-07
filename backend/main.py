from PWDWizard.MasterPassword import get_key_from_password
from PWDWizard.ProtectMasterAndSalt import load_or_create_salt
from PWDWizard.SQLite import create_db
from PWDWizard.SavingAndRetrieving import save_password, save_generated_password, get_passwords

def main():
    create_db()

    salt = load_or_create_salt()
    master_pw = input("Enter your master password: ")
    key = get_key_from_password(master_pw, salt)

    while True:
        print("\n1. Save Password")
        print("2. View Passwords")
        print("3. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            website = input("Website: ")
            user = input("Username: ")
            option = input("Type '1' to generate a password or '2' to enter your own: ")

            if option == "1":
                password = save_generated_password(website, user, key)
                print(f"Generated and saved password: {password}")
            elif option == "2":
                password = input("Enter the password to save: ")
                save_password(website, user, password, key)
                print("Password saved.")
            else:
                print("Invalid option.")

        elif choice == "2":
            get_passwords(key)

        elif choice == "3":
            break

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()