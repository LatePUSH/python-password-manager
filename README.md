## 🔐 Python Password Manager

A command-line password manager that securely stores credentials locally using symmetric encryption. 

**Main Features**
* **Secure Encryption**: Uses the `cryptography.fernet` library to encrypt all saved passwords.
* **Key Management**: Generate and load local encryption keys to lock and unlock your vault.
* **Interactive CLI**: Easy-to-use terminal menu for adding, retrieving, and displaying saved credentials.
* **Local Storage**: All data remains on your machine, eliminating third-party cloud risks.

**Prerequisites**
* Python 3.x
* `cryptography` module

**Installation & Usage**
1. Install the required dependency:
> pip install cryptography

2. Run the script:
> python gestionnaire.py

3. Follow the on-screen prompts to generate a key (e.g., `secret.key`), create a password file (e.g., `vault.txt`), and manage your credentials.

**⚠️ Security Warning**
Never commit your `.key` files or your personal password files to a public GitHub repository. Always keep them local.
