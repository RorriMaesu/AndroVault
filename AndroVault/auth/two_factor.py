# auth/two_factor.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import pyotp
import qrcode
from io import BytesIO
from PIL import Image, ImageTk
from constants import COLORS, FONT_NAME, FONT_SIZE, APP_NAME
from .utils import save_2fa_secret, load_2fa_secret, encrypt_data, decrypt_data
from logger import log_event, log_error

def create_qr_window(root, provisioning_uri, verify_callback):
    """Create a window to display the QR code for 2FA setup."""
    try:
        log_event("Creating QR code window")
        
        # Create QR display window
        qr_window = tk.Toplevel(root)
        qr_window.title("2FA Setup")
        qr_window.configure(bg=COLORS['BG_COLOR'])
        
        # Make window modal
        qr_window.transient(root)
        qr_window.grab_set()
        
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            box_size=4,  # Smaller box size
            border=2
        )
        qr.add_data(provisioning_uri)
        qr.make(fit=True)
        
        # Convert to PhotoImage
        qr_image = qr.make_image(fill_color="black", back_color="white")
        photo = ImageTk.PhotoImage(qr_image)
        
        # Create main container with padding
        main_frame = ttk.Frame(qr_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Title label with proper styling
        title_label = ttk.Label(
            main_frame,
            text="Two-Factor Authentication Setup",
            font=(FONT_NAME, FONT_SIZE + 2, 'bold'),
            background=COLORS['BG_COLOR']
        )
        title_label.pack(pady=(0, 20))
        
        # Instructions with proper styling
        ttk.Label(
            main_frame,
            text="Scan this QR code with your authenticator app\n(e.g., Google Authenticator)",
            justify=tk.CENTER,
            font=(FONT_NAME, FONT_SIZE),
            background=COLORS['BG_COLOR']
        ).pack(pady=(0, 20))
        
        # QR code display with frame and padding
        qr_frame = ttk.Frame(main_frame, padding=15)
        qr_frame.pack(pady=20)
        
        label = ttk.Label(qr_frame, image=photo, background=COLORS['BG_COLOR'])
        label.image = photo  # Keep reference
        label.pack(padx=20, pady=20)
        
        # Verify button with styling
        verify_button = ttk.Button(
            main_frame,
            text="Verify Code",
            command=lambda: verify_callback(qr_window),
            style='Accent.TButton',
            padding=(20, 10)
        )
        verify_button.pack(pady=(30, 0))
        
        # Set window size based on content
        qr_window.geometry("500x650")
        qr_window.minsize(500, 650)
        
        # Center window on screen
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - 500) // 2
        y = (screen_height - 650) // 2
        qr_window.geometry(f"500x650+{x}+{y}")
        
        # Prevent window resizing
        qr_window.resizable(False, False)
        
        # Force window to show at full size
        qr_window.update_idletasks()
        
        log_event("QR code window created successfully")
        return qr_window
        
    except Exception as e:
        log_error(f"Failed to create QR window: {str(e)}")
        messagebox.showerror("Error", "Failed to create QR code window.")
        return None

def verify_and_close(window, callback):
    """Execute verification callback and close window if successful"""
    try:
        log_event("Executing verification callback")
        if callback():
            log_event("Verification successful, closing window")
            window.destroy()
        else:
            log_event("Verification failed")
    except Exception as e:
        log_error(f"Error in verify_and_close: {str(e)}")

def verify_and_save_otp(qr_window, otp_secret, master_password):
    """Verify OTP and save the secret if valid."""
    try:
        user_otp = simpledialog.askstring(
            "Verify 2FA",
            "Enter the 6-digit code from Google Authenticator:",
            parent=qr_window,
            show='*'
        )
        
        if not user_otp:
            log_event("User cancelled 2FA verification")
            return False
            
        # Verify the OTP
        totp = pyotp.TOTP(otp_secret)
        if totp.verify(user_otp.strip()):
            # Encrypt and save the secret
            encrypted_secret = encrypt_data(otp_secret.encode(), master_password)
            if encrypted_secret and save_2fa_secret(encrypted_secret, master_password):
                messagebox.showinfo("Success", "2FA setup completed successfully!", parent=qr_window)
                log_event("2FA setup completed successfully")
                return True
                
        log_event("Invalid 2FA code entered")
        messagebox.showerror("Error", "Invalid code. Please try again.", parent=qr_window)
        return False
        
    except Exception as e:
        log_error(f"Failed to verify OTP: {str(e)}")
        messagebox.showerror("Error", "Failed to verify code.", parent=qr_window)
        return False

def verify_existing_2fa(root, master_password, encrypted_secret):
    """Verify 2FA for existing users."""
    try:
        # Decrypt the secret
        secret = decrypt_data(encrypted_secret, master_password)
        if not secret:
            log_error("Failed to decrypt 2FA secret")
            return False
            
        # Create TOTP object
        totp = pyotp.TOTP(secret.decode())
        
        # Get code from user
        code = simpledialog.askstring(
            "2FA Verification", 
            "Enter the 6-digit code from Google Authenticator:",
            parent=root,
            show='*'
        )
        
        if not code:
            log_event("User cancelled 2FA verification")
            return False
            
        # Verify the code
        if totp.verify(code.strip()):
            log_event("2FA verification successful")
            return True
            
        log_event("Invalid 2FA code entered")
        messagebox.showerror("Error", "Invalid code. Please try again.", parent=root)
        return False
        
    except Exception as e:
        log_error(f"Failed to verify 2FA: {str(e)}")
        messagebox.showerror("Error", "2FA verification failed.", parent=root)
        return False

def setup_2fa(root, master_password):
    """Set up 2FA for a new user."""
    try:
        log_event("Starting 2FA setup process")
        
        # Temporarily show root window for dialog
        root.deiconify()
        
        # Generate new secret and URI
        otp_secret = pyotp.random_base32()
        totp = pyotp.TOTP(otp_secret)
        provisioning_uri = totp.provisioning_uri(
            name="AndroVault User",
            issuer_name="AndroVault"
        )

        # Create QR window
        qr_window = tk.Toplevel(root)
        qr_window.title("2FA Setup")
        qr_window.transient(root)
        qr_window.grab_set()
        
        # Center the QR window
        window_width = 400
        window_height = 500
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        qr_window.geometry(f'{window_width}x{window_height}+{x}+{y}')

        # Generate QR code
        qr = qrcode.QRCode(version=1, box_size=4, border=5)
        qr.add_data(provisioning_uri)
        qr.make(fit=True)
        qr_image = qr.make_image(fill_color="black", back_color="white")
        photo = ImageTk.PhotoImage(qr_image)

        # Display instructions and QR code
        ttk.Label(
            qr_window,
            text="Scan this QR code with your authenticator app\n(e.g., Google Authenticator)",
            justify=tk.CENTER
        ).pack(pady=10)

        label = ttk.Label(qr_window, image=photo)
        label.image = photo  # Keep reference!
        label.pack(padx=20, pady=10)

        success = [False]  # Use list to modify in nested function

        def verify_otp():
            code = simpledialog.askstring(
                "Verify 2FA",
                "Enter the code from your authenticator app:",
                parent=qr_window
            )
            
            if code and totp.verify(code.strip()):
                # Encrypt and save the secret
                encrypted_secret = encrypt_data(otp_secret.encode(), master_password)
                if save_2fa_secret(encrypted_secret, master_password):
                    log_event("2FA secret saved successfully")
                    messagebox.showinfo("Success", "2FA setup completed successfully!")
                    success[0] = True
                    qr_window.destroy()
            else:
                messagebox.showerror("Error", "Invalid code. Please try again.")

        ttk.Button(
            qr_window,
            text="Verify Code",
            command=verify_otp
        ).pack(pady=10)

        # Wait for window to be destroyed
        root.wait_window(qr_window)
        
        # Hide root window again
        root.withdraw()
        
        # Return success status
        return success[0]

    except Exception as e:
        log_error(f"Failed to setup 2FA: {str(e)}")
        messagebox.showerror("Error", "Failed to setup 2FA.")
        root.withdraw()
        return False

def verify_2fa(root, master_password):
    """Verify 2FA or set it up if not configured."""
    try:
        log_event("Starting 2FA verification process")
        encrypted_secret = load_2fa_secret(master_password)
        
        # For testing/development - always show QR code
        log_event("Starting fresh 2FA setup")
        return setup_2fa(root, master_password)

    except Exception as e:
        log_error(f"2FA verification process failed: {str(e)}")
        messagebox.showerror("Error", "2FA verification failed.", parent=root)
        return False
