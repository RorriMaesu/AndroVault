from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import base64
import os

def derive_key(password: str, salt: bytes = None) -> bytes:
    """Derive encryption key from password"""
    if salt is None:
        salt = os.urandom(16)
    password = password.encode()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(password))

def encrypt_data(data: bytes, key: str) -> bytes:
    """Encrypt data using key"""
    try:
        if not isinstance(data, bytes):
            raise ValueError("Data must be bytes")
            
        # Generate encryption key from password
        fernet = Fernet(derive_key(key))
        
        # Encrypt data
        return fernet.encrypt(data)
        
    except Exception as e:
        log_error(f"Failed to encrypt data: {str(e)}")
        raise

def decrypt_data(encrypted_data: bytes, key: str) -> bytes:
    """Decrypt data using key"""
    try:
        if not isinstance(encrypted_data, bytes):
            raise ValueError("Encrypted data must be bytes")
            
        # Generate encryption key from password
        fernet = Fernet(derive_key(key))
        
        # Decrypt data
        return fernet.decrypt(encrypted_data)
        
    except Exception as e:
        log_error(f"Failed to decrypt data: {str(e)}")
        raise