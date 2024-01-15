import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import secrets
import string


def generate_secure_random_string(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    random_string = ''.join(secrets.choice(characters) for _ in range(length))
    return random_string


def generate_key(secret, salt=b'J;@?pT,"/I8l${iC.]x2PS:@e]XNP>\'i!$!L,K)jY=_d#q},}Y$G@N0fB)e7UB@8'):
    secret_b = secret.encode()
    # salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(secret_b))
    return key


def write_key(secret, salt):
    random_key = generate_key(secret, salt)
    with open("keyFile.key", "wb") as key_file:
        key_file.write(random_key)
    try:
        os.system(f'attrib +h "keyFile.key"')
    except Exception as e:
        print(f"Error setting hidden attribute: {e}")


class NoPasswordException(Exception):
    pass


class PasswordDoNotMatch(Exception):
    pass


# print(generate_key("2"))
# print(generate_key("4"))

def load_key():
    with open("keyFile.key", "rb") as key_file:
        key = key_file.read()
    return key


class PasswordManager:
    def __init__(self):
        self.pwd = None
        self.key = None
        self.fer = None
        self.salt = None

    def add(self):
        if self.pwd is None:
            raise NoPasswordException("No master password was entered")
        if self.key is None:
            user_key = generate_key(self.pwd, self.salt)
            actual_key = load_key()
            if user_key != actual_key:
                raise PasswordDoNotMatch("Unable to decrypt, wrong master password.")
            self.key = user_key
            self.fer = Fernet(self.key)
        url = input("url: ")
        username = input("username: ")
        password = input("password: ")
        encrypted_pass = self.fer.encrypt(password.encode()).decode()
        with open("password_entries.txt", "a") as f:
            f.write(f"{url} | {username} | {encrypted_pass} \n")
        print("\nEntry added successfully")

    def view(self):
        if self.pwd is None:
            raise NoPasswordException("No master password was entered")
        if self.key is None:
            user_key = generate_key(self.pwd, self.salt)
            actual_key = load_key()
            if user_key != actual_key:
                raise PasswordDoNotMatch("Unable to decrypt, wrong master password.")
            self.key = user_key
            self.fer = Fernet(self.key)
        if not os.path.exists("password_entries.txt"):
            print("No entries to show, please first enter some...")
            return
        with open("password_entries.txt", "r") as f:
            for line in f.readlines():
                (url, username, encrypted_pass) = line.rstrip().split(' | ')
                try:
                    password = self.fer.decrypt(encrypted_pass).decode()
                    print(f"URL: {url}\nUsername: {username} | Password: {password}")
                    print("-" * 40, "\n")
                except Exception as error:
                    print(error)
                    raise PasswordDoNotMatch("Unable to decrypt, wrong master password.")


password_manager = PasswordManager()

while True:
    if os.path.exists(".info"):
        print("\n******** Password Manager Menu ********\n")
        if password_manager.pwd is None:
            with open(".info", "rb") as f:
                salt = f.readline()
            pwd = input("Please enter your master password: ")
            password_manager.pwd = pwd
            password_manager.salt = salt
        mode = int(input("1. Enter new entry\n2. View entry(s)\nAny other to exit\n"))
        if mode == 1:
            try:
                password_manager.add()
            except NoPasswordException as error:
                print(error)
                pwd = input("Please enter your master password: ")
                password_manager.pwd = pwd
            except PasswordDoNotMatch as error:
                print(error)
                print("Master password do not match, please try again\n")
                pwd = input("Please enter your master password: ")
                password_manager.pwd = pwd
        elif mode == 2:
            try:
                password_manager.view()
            except NoPasswordException as error:
                print(error)
                pwd = input("Please enter your master password: ")
                password_manager.pwd = pwd
            except PasswordDoNotMatch as error:
                print(error)
                print("Master password do not match, please try again\n")
                pwd = input("Please enter your master password: ")
                password_manager.pwd = pwd
        else:
            print("Exiting...")
            break
    else:
        print("Welcome to Password Management System\nBy - Shishank Rawat\n")
        user = input("What should we call you?\n")
        print(f"Ok, Welcome again {user} 😁!")
        master_pwd = input("Enter Master Password for your entries: ")
        salt = generate_secure_random_string(64).encode()
        write_key(master_pwd, salt)
        password_manager.pwd = master_pwd
        password_manager.salt = salt
        f = open(".info", "wb")
        f.write(salt)
        f.close()

        print("Please remember this password for future purposes...")
        try:
            os.system(f'attrib +h ".info"')
        except Exception as e:
            print(f"Error setting hidden attribute: {e}")