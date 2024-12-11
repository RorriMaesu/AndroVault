# auth/utils.py
import os
import bcrypt
from tkinter import simpledialog, messagebox
from logger import log_error, log_event
from cryptography.fernet import Fernet
from utils.password_utils import encrypt_data, decrypt_data

MASTER_PASSWORD_FILE = "master.hash"
TWO_FA_FILE = "2fa.key"

def load_master_password():
    """Load and verify the master password hash."""
    try:
        if not os.path.exists(MASTER_PASSWORD_FILE):
            log_event("No master password file found")
            return None
        with open(MASTER_PASSWORD_FILE, "rb") as f:
            stored_hash = f.read()
        return stored_hash
    except Exception as e:
        log_error(f"Failed to load master password: {str(e)}")
        return None

def set_master_password(password_hash: bytes) -> bool:
    """Save the master password hash."""
    try:
        with open(MASTER_PASSWORD_FILE, "wb") as f:
            f.write(password_hash)
        log_event("Master password hash saved successfully")
        return True
    except Exception as e:
        log_error(f"Failed to save master password: {str(e)}")
        return False

def hash_password(password: str) -> bytes:
    """Hash a password using bcrypt."""
    try:
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode(), salt)
        log_event("Password hashed successfully")
        return password_hash
    except Exception as e:
        log_error(f"Failed to hash password: {str(e)}")
        return None

def verify_password(password: str, stored_hash: bytes) -> bool:
    """Verify a password against its hash."""
    try:
        result = bcrypt.checkpw(password.encode(), stored_hash)
        log_event("Password verification completed")
        return result
    except Exception as e:
        log_error(f"Password verification failed: {str(e)}")
        return False

def get_new_master_password(root):
    """Get and confirm new master password."""
    try:
        while True:
            password = simpledialog.askstring(
                "Set Master Password",
                "Enter new master password:",
                parent=root,
                show='*'
            )
            
            if not password:
                log_event("Master password setup cancelled")
                return None
                
            # Confirm password
            confirm = simpledialog.askstring(
                "Confirm Master Password",
                "Confirm new master password:",
                parent=root,
                show='*'
            )
            
            if password == confirm:
                log_event("New master password confirmed")
                return password
            else:
                log_event("Master password confirmation failed")
                messagebox.showerror(
                    "Error",
                    "Passwords do not match. Please try again.",
                    parent=root
                )
    except Exception as e:
        log_error(f"Failed to get new master password: {str(e)}")
        return None

def get_master_password_input(root):
    """Get master password input from user."""
    try:
        password = simpledialog.askstring(
            "Master Password",
            "Enter your master password:",
            parent=root,
            show='*'
        )
        if password:
            log_event("Master password input received")
        else:
            log_event("Master password input cancelled")
        return password
    except Exception as e:
        log_error(f"Failed to get master password input: {str(e)}")
        return None

def save_2fa_secret(encrypted_secret, master_password):
    """Save the encrypted 2FA secret."""
    try:
        with open(TWO_FA_FILE, "wb") as f:
            f.write(encrypted_secret)
        log_event("2FA secret saved successfully")
        return True
    except Exception as e:
        log_error(f"Failed to save 2FA secret: {str(e)}")
        return False

def load_2fa_secret(master_password):
    """Load the encrypted 2FA secret."""
    try:
        if not os.path.exists(TWO_FA_FILE):
            log_event("No existing 2FA secret found")
            return None
        with open(TWO_FA_FILE, "rb") as f:
            return f.read()
    except Exception as e:
        log_error(f"Failed to load 2FA secret: {str(e)}")
        return None
