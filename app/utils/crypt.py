from cryptography.fernet import Fernet
from config import APP_SECRET  
import base64

if len(APP_SECRET) != 32:
    raise ValueError("APP_SECRET must be exactly 32 characters long!")

def encrypt(string: str, key=None) -> bytes:
    key = key if key else APP_SECRET
    key = base64.urlsafe_b64encode(key.encode()) 

    cipher = Fernet(key)
    encrypted_string = cipher.encrypt(string.encode())
    return encrypted_string

def decrypt(encrypted_string: bytes, key=None) -> str:
    key = key if key else APP_SECRET
    key = base64.urlsafe_b64encode(key.encode()) 

    cipher = Fernet(key)
    decrypted_string = cipher.decrypt(encrypted_string).decode()
    return decrypted_string

