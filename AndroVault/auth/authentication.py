# auth/authentication.py
import tkinter as tk
from tkinter import simpledialog, messagebox
from .two_factor import verify_2fa, setup_2fa
from .utils import load_master_password, set_master_password, hash_password, verify_password, get_new_master_password, get_master_password_input
from logger import log_event, log_error
import os
from constants import MASTER_PASSWORD_FILE

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
                return password
            else:
                messagebox.showerror("Error", "Passwords do not match. Please try again.", parent=root)
                
    except Exception as e:
        log_error(f"Failed to get new master password: {str(e)}")
        return None

def authenticate(root):
    """Main authentication function."""
    try:
        log_event("Starting authentication process")
        master_password = None
        
        # Check if master password file exists
        if not os.path.exists(MASTER_PASSWORD_FILE):
            log_event("No master password found, initiating first-time setup")
            # Get new master password
            master_password = get_new_master_password(root)
            if not master_password:
                log_event("Master password setup cancelled")
                return None
                
            # Hash and save the new password
            password_hash = hash_password(master_password)
            if not password_hash or not set_master_password(password_hash):
                log_error("Failed to hash and save master password")
                messagebox.showerror("Error", "Failed to save master password.")
                return None
                
            log_event("New master password created successfully")
        else:
            # Existing user flow
            log_event("Existing master password found, verifying")
            stored_hash = load_master_password()
            if not stored_hash:
                log_error("Failed to load master password hash")
                return None
                
            master_password = get_master_password_input(root)
            if not master_password:
                log_event("Master password input cancelled")
                return None
                
            if not verify_password(master_password, stored_hash):
                log_event("Invalid master password entered")
                messagebox.showerror("Authentication Failed", "Invalid master password.", parent=root)
                return None
                
            log_event("Master password verified successfully")
        
        # 2FA Setup/Verification
        if not verify_2fa(root, master_password):
            log_event("2FA setup/verification failed")
            return None
            
        log_event("Authentication completed successfully")
        return master_password
        
    except Exception as e:
        log_error(f"Authentication process failed: {str(e)}")
        messagebox.showerror("Error", "Authentication failed due to an unexpected error.", parent=root)
        return None
