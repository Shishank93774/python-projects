# Password Manager Application

This is a simple yet secure command-line password manager application built using Python. It allows you to securely store, encrypt, and retrieve your passwords using a master password.

## Features

- **Secure Storage:** Passwords are encrypted using AES-256 encryption provided by the `cryptography` library.
- **Master Password:** A master password is used to encrypt and decrypt your stored passwords.
- **Random String Generation:** The application can generate secure random strings for use as salts or passwords.
- **Error Handling:** Custom exceptions ensure that errors like mismatched passwords or missing files are handled gracefully.
- **File Hiding:** Key and information files are hidden to prevent accidental exposure.

## Requirements

- Python 3.6+
- The necessary Python packages are listed in `requirements.txt`.

You can install the required dependencies using the following command:

```bash
pip install -r requirements.txt
```

## How to Use

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/Shishank93774/python-projects.git
    cd password-manager
    ```

2. **Install Dependencies:**

    Install the necessary Python packages using `requirements.txt`:

    ```bash
    pip install -r requirements.txt
    ```

3. **Run the Application:**

    Run the `password_manager.py` file to start the application.

    ```bash
    python main.py
    ```

4. **First-Time Setup:**

    - On your first run, you'll be prompted to set a master password.
    - A unique salt will be generated, and a key will be derived using the PBKDF2HMAC algorithm.
    - The key is stored in a hidden file called `keyFile.key`.
    - The salt used for key derivation is stored in a hidden `.info` file.

5. **Add a New Password:**

    - Select option `1` from the menu to add a new password entry.
    - You'll be asked to enter the URL, username, and password.
    - The password is encrypted and stored securely.

6. **View Stored Passwords:**

    - Select option `2` from the menu to view stored passwords.
    - You'll be asked to enter your master password for decryption.
    - If the master password matches, the stored passwords will be decrypted and displayed.

7. **Exiting the Application:**

    - Select any other number in the menu to exit the application.

## Project Structure

```plaintext
password-manager/
│
├── main.py    # The main application file
├── keyFile.key            # Hidden key file (automatically generated)
├── .info                  # Hidden salt file (automatically generated)
└── requirements.txt       # List of Python dependencies
```

## Security Considerations

- **Master Password:** The security of your stored passwords is entirely dependent on the strength of your master password. Choose a strong and unique master password.
- **File Protection:** The key file and salt file are hidden to avoid accidental exposure. Ensure these files are not deleted or altered, as they are crucial for decrypting your stored passwords.
- **Encryption:** The passwords are encrypted using AES-256, a strong and widely accepted encryption standard.

## Customization
- You can customize the length and characters used in the random string generator by modifying the `generate_secure_random_string` function.
- The number of iterations and the hashing algorithm used in the PBKDF2HMAC key derivation can be adjusted in the `generate_key` function.

## Contributing
Contributions are welcome! If you find any issues or have suggestions for improvement, feel free to open an issue or submit a pull request.

## Author
- **Shishank Rawat**