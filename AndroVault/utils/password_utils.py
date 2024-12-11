# utils/password_utils.py
import secrets
import string
from tkinter import messagebox
from constants import COLORS
from logger import log_error
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
import base64
import os

def generate_password(length=16):
    try:
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(secrets.choice(characters) for _ in range(length))
        return password
    except Exception as e:
        log_error(f"Failed to generate password: {str(e)}")
        return None

def evaluate_strength(password):
    try:
        strength = 0
        if len(password) >= 8:
            strength += 1
        if any(c.isupper() for c in password):
            strength += 1
        if any(c.islower() for c in password):
            strength += 1
        if any(c.isdigit() for c in password):
            strength += 1
        if any(not c.isalnum() for c in password):
            strength += 1

        strength_levels = ["Very Weak", "Weak", "Medium", "Strong", "Very Strong"]
        colors = ["red", "orange", "yellow", "blue", "green"]
        return strength_levels[min(strength, 4)], colors[min(strength, 4)]
    except Exception as e:
        log_error(f"Failed to evaluate password strength: {str(e)}")
        return "", "black"

def derive_key(master_password: str, salt: bytes = None) -> bytes:
    """Derive a secret key from the master password using PBKDF2."""
    try:
        if not salt:
            salt = os.urandom(16)  # Generate a new salt
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100_000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
        return key, salt
    except Exception as e:
        log_error(f"Failed to derive key: {str(e)}")
        return None, None

def encrypt_data(data: bytes, master_password: str) -> bytes:
    """Encrypt data using a key derived from the master password."""
    try:
        key, salt = derive_key(master_password)
        if not key:
            return None
        fernet = Fernet(key)
        encrypted = fernet.encrypt(data)
        # Prepend salt to encrypted data for later key derivation
        return salt + encrypted
    except Exception as e:
        log_error(f"Failed to encrypt data: {str(e)}")
        return None

def decrypt_data(encrypted_data: bytes, master_password: str) -> bytes:
    """Decrypt data using a key derived from the master password."""
    try:
        salt = encrypted_data[:16]
        encrypted = encrypted_data[16:]
        key, _ = derive_key(master_password, salt)
        if not key:
            return None
        fernet = Fernet(key)
        decrypted = fernet.decrypt(encrypted)
        return decrypted
    except Exception as e:
        log_error(f"Failed to decrypt data: {str(e)}")
        return None
