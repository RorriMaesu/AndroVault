import tkinter as tk
from tkinter import ttk
import constants
from logger import log_event, log_error
from auth.authentication import verify_password

class LoginWindow:
    def __init__(self, root, login_callback):
        """Initialize login window."""
        self.root = root
        self.login_callback = login_callback
        self.window = tk.Toplevel(root)
        self.setup_window()
        self.create_widgets()

    def setup_window(self):
        """Configure login window."""
        self.window.title("Login - AndroVault")
        self.window.geometry("400x300")
        self.window.resizable(False, False)
        
        # Center window
        self.window.transient(self.root)
        self.window.grab_set()
        
        # Configure style
        style = ttk.Style()
        style.configure(
            "Login.TFrame",
            background=constants.COLORS['bg']
        )

    def create_widgets(self):
        """Create login form widgets."""
        # Main container
        main_frame = ttk.Frame(
            self.window,
            padding=constants.PADDING['large'],
            style="Login.TFrame"
        )
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        ttk.Label(
            main_frame,
            text="Welcome to AndroVault",
            font=constants.FONTS['heading']
        ).pack(pady=(0, 20))

        # Password field
        ttk.Label(
            main_frame,
            text="Master Password:",
            font=constants.FONTS['default']
        ).pack(fill=tk.X)
        
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(
            main_frame,
            textvariable=self.password_var,
            show="•",
            font=constants.FONTS['default']
        )
        self.password_entry.pack(fill=tk.X, pady=(5, 20))

        # Login button
        ttk.Button(
            main_frame,
            text="Login",
            command=self.handle_login,
            style="Accent.TButton"
        ).pack(fill=tk.X)

        # Error message
        self.error_var = tk.StringVar()
        self.error_label = ttk.Label(
            main_frame,
            textvariable=self.error_var,
            foreground=constants.COLORS['error'],
            font=constants.FONTS['small']
        )
        self.error_label.pack(pady=(10, 0))

        # Focus password field
        self.password_entry.focus()
        self.window.bind('<Return>', lambda e: self.handle_login())

    def handle_login(self):
        """Process login attempt."""
        try:
            password = self.password_var.get()
            
            if not password:
                self.show_error("Please enter your master password")
                return

            if verify_password(password):
                log_event("Login successful")
                self.window.destroy()
                if self.login_callback(password):
                    return
            
            self.show_error("Invalid master password")
            self.password_var.set("")
            self.password_entry.focus()

        except Exception as e:
            log_error(f"Login failed: {str(e)}")
            self.show_error("Login failed. Please try again.")

    def show_error(self, message):
        """Display error message."""
        self.error_var.set(message) 