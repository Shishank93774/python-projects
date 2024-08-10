import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import secrets
import string


def generate_secure_random_string(length: int) -> str:
    """
    Generates a secure random string of the specified length using a combination
    of ASCII letters, digits, and punctuation.

    Args:
        length (int): The length of the generated string.

    Returns:
        str: A secure random string of the specified length.
    """
    characters = string.ascii_letters + string.digits + string.punctuation
    random_string = ''.join(secrets.choice(characters) for _ in range(length))
    return random_string


def generate_key(secret: str, salt: bytes) -> bytes:
    """
    Derives a key from the secret and salt using PBKDF2HMAC.
    The derived key is used for encryption and decryption.

    Args:
        secret (str): The master password provided by the user.
        salt (bytes): A unique salt value to enhance security.

    Returns:
        bytes: A base64-encoded key derived from the secret and salt.
    """
    secret_b = secret.encode()  # Convert the secret to bytes
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(secret_b))
    return key


def write_key(secret: str, salt: bytes) -> None:
    """
    Generates an encryption key using the provided secret and salt,
    writes the key to a file, and hides the file.

    Args:
        secret (str): The master password provided by the user.
        salt (bytes): A unique salt value to enhance security.
    """
    try:
        random_key = generate_key(secret, salt)
        with open("keyFile.key", "wb") as key_file:
            key_file.write(random_key)
        os.system(f'attrib +h "keyFile.key"')  # Hide the key file
    except Exception as e:
        print(f"Error while writing or hiding the key file: {e}")


class NoPasswordException(Exception):
    """Exception raised when no master password is entered."""
    pass


class PasswordDoNotMatch(Exception):
    """Exception raised when the entered password does not match the stored key."""
    pass


def load_key() -> bytes:
    """
    Loads the encryption key from the key file.

    Returns:
        bytes: The encryption key.

    Raises:
        FileNotFoundError: If the key file does not exist.
    """
    try:
        with open("keyFile.key", "rb") as key_file:
            key = key_file.read()
        return key
    except FileNotFoundError:
        raise FileNotFoundError("Key file not found. Ensure the key file is in place.")


class PasswordManager:
    """
    Manages password storage and retrieval using encryption.
    The master password is used to generate a key for encrypting and decrypting entries.
    """

    def __init__(self):
        """Initializes the PasswordManager with default values for password, key, and salt."""
        self.pwd: str | None = None
        self.key: bytes | None = None
        self.fer: Fernet | None = None
        self.salt: bytes | None = None

    def add(self) -> None:
        """
        Adds a new password entry after validating the master password.
        The entry is encrypted and stored in a file.

        Raises:
            NoPasswordException: If no master password is provided.
            PasswordDoNotMatch: If the entered password does not match the stored key.
        """
        if self.pwd is None:
            raise NoPasswordException("No master password was entered")

        if self.key is None:
            # Generate the key using the provided password and salt
            user_key = generate_key(self.pwd, self.salt)
            actual_key = load_key()
            if user_key != actual_key:
                raise PasswordDoNotMatch("Unable to decrypt, wrong master password.")
            self.key = user_key
            self.fer = Fernet(self.key)

        url = input("URL: ")
        username = input("Username: ")
        password = input("Password: ")

        try:
            # Encrypt the password before saving
            encrypted_pass = self.fer.encrypt(password.encode()).decode()
            with open("password_entries.txt", "a") as f:
                f.write(f"{url} | {username} | {encrypted_pass}\n")
            print("\nEntry added successfully")
        except Exception as e:
            print(f"Error while adding entry: {e}")

    def view(self) -> None:
        """
        Views and decrypts stored password entries.
        The entries are decrypted using the master password.

        Raises:
            NoPasswordException: If no master password is provided.
            PasswordDoNotMatch: If the entered password does not match the stored key.
        """
        if self.pwd is None:
            raise NoPasswordException("No master password was entered")

        if self.key is None:
            # Generate the key using the provided password and salt
            user_key = generate_key(self.pwd, self.salt)
            actual_key = load_key()
            if user_key != actual_key:
                raise PasswordDoNotMatch("Unable to decrypt, wrong master password.")
            self.key = user_key
            self.fer = Fernet(self.key)

        if not os.path.exists("password_entries.txt"):
            print("No entries to show, please first enter some...")
            return

        try:
            # Read and decrypt each entry
            with open("password_entries.txt", "r") as f:
                for line in f.readlines():
                    url, username, encrypted_pass = line.rstrip().split(' | ')
                    password = self.fer.decrypt(encrypted_pass.encode()).decode()
                    print(f"URL: {url}\nUsername: {username} | Password: {password}")
                    print("-" * 40, "\n")
        except Exception as error:
            print(f"Error while viewing entries: {error}")
            raise PasswordDoNotMatch("Unable to decrypt, wrong master password.")


password_manager = PasswordManager()

# Main loop to handle user interaction
while True:
    if os.path.exists(".info"):
        print("\n******** Password Manager Menu ********\n")
        if password_manager.pwd is None:
            try:
                with open(".info", "rb") as f:
                    salt = f.readline()
                pwd = input("Please enter your master password: ")
                password_manager.pwd = pwd
                password_manager.salt = salt
            except Exception as e:
                print(f"Error loading salt or reading master password: {e}")
                continue

        try:
            mode = int(input("1. Enter new entry\n2. View entry(s)\nAny other to exit\n"))
            if mode == 1:
                password_manager.add()
            elif mode == 2:
                password_manager.view()
            else:
                print("Exiting...")
                break
        except ValueError:
            print("Invalid input, please enter a valid number.")
        except NoPasswordException as error:
            print(error)
            password_manager.pwd = input("Please enter your master password: ")
        except PasswordDoNotMatch as error:
            print(error)
            print("Master password does not match, please try again\n")
            password_manager.pwd = input("Please enter your master password: ")
    else:
        print("Welcome to Password Management System\nBy - Shishank Rawat\n")
        user = input("What should we call you?\n")
        print(f"Ok, Welcome again {user} 😁!")
        master_pwd = input("Enter Master Password for your entries: ")
        salt = generate_secure_random_string(64).encode()

        try:
            write_key(master_pwd, salt)
            password_manager.pwd = master_pwd
            password_manager.salt = salt
            with open(".info", "wb") as f:
                f.write(salt)
            os.system(f'attrib +h ".info"')  # Hide the .info file
            print("Please remember this password for future purposes...")
        except Exception as e:
            print(f"Error during initial setup: {e}")