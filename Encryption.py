import io
import os
import csv
from pathlib import Path
from cryptography.fernet import Fernet


FILES_PATH = Path("C:/Users/simon/Desktop/Python_files")
KEY_FILE = FILES_PATH / "key.key"
ORIGINAL_FILE = FILES_PATH / "password.csv"
ENCRYPTED_FILE = FILES_PATH / "password_encrypted.csv"


def create_key():
    key = Fernet.generate_key()  # store in a secure location
    print("Key:", key.decode())
    return key


def encrypt(message: bytes, key: bytes) -> bytes:
    return Fernet(key).encrypt(message)


def decrypt(token: bytes, key: bytes) -> bytes:
    return Fernet(key).decrypt(token)


def get_file(file_path, read=True):
    with open(file_path, 'r') as file:
        if read:
            return file.read()
        else:
            return file


def get_file_binary(file_path, read=True):
    with open(file_path, 'rb') as file:
        if read:
            return file.read()
        else:
            return file


def write_file(content, file):
    file_path, file_extension = os.path.splitext(file)
    with open(file_path + '_encrypted' + file_extension, 'wb+') as new_file:
        new_file.write(content)


def encrypt(encryption_file=ORIGINAL_FILE, key_file=KEY_FILE):
    key = get_file_binary(key_file)
    fernet = Fernet(key)
    file_content = get_file_binary(encryption_file)
    encrypted = fernet.encrypt(file_content)
    write_file(encrypted, encryption_file)
    file_path, file_extension = os.path.splitext(encryption_file)
    with open(file_path + '_encrypted' + file_extension, 'wb+') as new_file:
        new_file.write(encrypted)
    return encrypted.decode()


def decrypt(file=ENCRYPTED_FILE, key_file=KEY_FILE):
    key = get_file_binary(key_file)
    fernet = Fernet(key)
    file_content = get_file_binary(file)
    decrypted = fernet.decrypt(file_content)
    return decrypted.decode()


def get_emails(cvs_file=decrypt(ENCRYPTED_FILE, KEY_FILE)):
    dict_reader = csv.DictReader(io.StringIO(cvs_file))
    lists = []
    for row in dict_reader:
        lists.append([row['email'], row['password'], row['imap']])
    return lists


if __name__ == "__main__":
    print(get_emails())
    exit()
    encrypt(ORIGINAL_FILE, KEY_FILE)
    emails = get_emails(decrypt(ENCRYPTED_FILE, KEY_FILE))


