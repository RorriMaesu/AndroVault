import tkinter as tk
from tkinter import ttk
import string
import secrets
from logger import log_event, log_error
from utils.error_handler import ErrorHandler
from .tooltip import create_tooltip

error_handler = ErrorHandler()

class PasswordGenerator(ttk.Frame):
    def __init__(self, parent, password_callback=None, clipboard_manager=None):
        """Initialize password generator."""
        super().__init__(parent)
        self.password_callback = password_callback
        self.clipboard_manager = clipboard_manager
        self.error_handler = ErrorHandler()
        self.setup_widgets()

    def setup_widgets(self):
        # Options frame
        options_frame = ttk.Frame(self)
        options_frame.pack(fill=tk.X, padx=5, pady=5)

        # Length selector
        ttk.Label(options_frame, text="Length:").pack(side=tk.LEFT)
        self.length_var = tk.StringVar(value="16")
        length_spin = ttk.Spinbox(
            options_frame,
            from_=8,
            to=64,
            width=3,
            textvariable=self.length_var
        )
        length_spin.pack(side=tk.LEFT, padx=(5, 10))
        create_tooltip(length_spin, "Password length (8-64 characters)")

        # Character type checkboxes
        self.use_upper = tk.BooleanVar(value=True)
        self.use_lower = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_special = tk.BooleanVar(value=True)

        ttk.Checkbutton(
            options_frame,
            text="A-Z",
            variable=self.use_upper
        ).pack(side=tk.LEFT, padx=2)

        ttk.Checkbutton(
            options_frame,
            text="a-z",
            variable=self.use_lower
        ).pack(side=tk.LEFT, padx=2)

        ttk.Checkbutton(
            options_frame,
            text="0-9",
            variable=self.use_digits
        ).pack(side=tk.LEFT, padx=2)

        ttk.Checkbutton(
            options_frame,
            text="!@#",
            variable=self.use_special
        ).pack(side=tk.LEFT, padx=2)

        # Generate button
        generate_btn = ttk.Button(
            options_frame,
            text="Generate",
            command=self.generate_password,
            style='Accent.TButton'
        )
        generate_btn.pack(side=tk.LEFT, padx=(10, 0))
        create_tooltip(generate_btn, "Generate a new password")

    def generate_password(self):
        """Generate a password based on selected options."""
        try:
            # Build character set
            chars = ''
            if self.use_upper.get():
                chars += string.ascii_uppercase
            if self.use_lower.get():
                chars += string.ascii_lowercase
            if self.use_digits.get():
                chars += string.digits
            if self.use_special.get():
                chars += string.punctuation

            if not chars:
                chars = string.ascii_letters + string.digits

            # Generate password
            length = int(self.length_var.get())
            password = ''.join(secrets.choice(chars) for _ in range(length))

            # Copy to clipboard if manager available
            if self.clipboard_manager:
                success = self.clipboard_manager.copy_to_clipboard(
                    password,
                    "Password copied to clipboard"
                )
                if not success:
                    log_error("Failed to copy password to clipboard")
            else:
                log_error("No clipboard manager available")

            # Call callback with new password
            if self.password_callback:
                self.password_callback(password)
                log_event("Password generated successfully")

        except Exception as e:
            self.error_handler.handle_error(e, "Failed to generate password") 