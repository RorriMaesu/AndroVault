# ui/account_detail.py
import tkinter as tk
from tkinter import ttk
import constants
from .tooltip import create_tooltip
from .password_generator import PasswordGenerator
from .password_strength import PasswordStrength
from .password_history import PasswordHistory
from logger import log_event, log_error, log_debug
from datetime import datetime
from .feedback import Feedback

class AccountDetail(ttk.Frame):
    def __init__(self, parent, account_manager, feedback_callback, clipboard_manager):
        """Initialize account detail form."""
        super().__init__(parent)
        self.account_manager = account_manager
        self.feedback_callback = feedback_callback
        self.clipboard_manager = clipboard_manager
        
        # Initialize variables first
        self.setup_variables()
        # Setup widgets
        self.setup_widgets()

    def setup_variables(self):
        """Initialize form variables."""
        self.website_var = tk.StringVar()
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.show_password = tk.BooleanVar()

    def set_password(self, password):
        """Set password in the password field."""
        try:
            self.password_var.set(password)
            log_event("Password set in form")
        except Exception as e:
            log_error(f"Failed to set password: {str(e)}")

    def setup_widgets(self):
        """Create form widgets."""
        # Main container
        main_frame = ttk.Frame(self, padding=constants.PADDING['medium'])
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Website field
        ttk.Label(main_frame, text="Website:", font=constants.FONTS['default']).pack(fill=tk.X)
        self.website_entry = ttk.Entry(main_frame, textvariable=self.website_var)
        self.website_entry.pack(fill=tk.X, pady=(0, 10))

        # Username field
        ttk.Label(main_frame, text="Username:", font=constants.FONTS['default']).pack(fill=tk.X)
        self.username_entry = ttk.Entry(main_frame, textvariable=self.username_var)
        self.username_entry.pack(fill=tk.X, pady=(0, 10))

        # Password field
        ttk.Label(main_frame, text="Password:", font=constants.FONTS['default']).pack(fill=tk.X)
        password_frame = ttk.Frame(main_frame)
        password_frame.pack(fill=tk.X, pady=(0, 5))
        
        self.password_entry = ttk.Entry(
            password_frame,
            textvariable=self.password_var,
            show="•"
        )
        self.password_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Initialize password generator after variables are set
        self.password_generator = PasswordGenerator(
            main_frame,
            self.set_password,
            self.clipboard_manager
        )
        self.password_generator.pack(fill=tk.X, pady=5)

        # Show/Hide password
        ttk.Checkbutton(
            password_frame,
            text="Show",
            variable=self.show_password,
            command=self._toggle_password_visibility
        ).pack(side=tk.LEFT, padx=5)

        # Password strength meter
        self.password_strength = PasswordStrength(main_frame)
        self.password_strength.pack(fill=tk.X, pady=5)

        # Password history
        history_frame = ttk.LabelFrame(
            main_frame,
            text="Password History",
            padding=constants.PADDING['small']
        )
        history_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.password_history = PasswordHistory(
            history_frame, 
            self.account_manager
        )
        self.password_history.pack(fill=tk.BOTH, expand=True)

        # Bind password changes to strength meter
        self.password_var.trace('w', self._on_password_change)

    def _toggle_password_visibility(self):
        """Toggle password visibility."""
        self.password_entry.configure(
            show="" if self.show_password.get() else "•"
        )

    def _on_password_generated(self, password):
        """Handle generated password."""
        try:
            self.password_var.set(password)
            self.show_feedback("Password generated", "success")
        except Exception as e:
            log_error(f"Password generation callback error: {str(e)}")
            self.show_feedback("Failed to set password", "error")

    def _on_password_change(self, *args):
        """Handle password changes."""
        password = self.password_var.get()
        self.password_strength.update_strength(password)

    def load_account(self, account):
        """Load account data into form."""
        try:
            self.current_account = account  # Store the full account data
            self.website_var.set(account['website'])
            self.username_var.set(account['username'])
            self.password_var.set(account['password'])
            if hasattr(self, 'notes_text'):
                self.notes_text.delete('1.0', tk.END)
                self.notes_text.insert('1.0', account.get('notes', ''))
            self.enable()
            log_event(f"Account loaded: {account['id']}")
            return True
        except Exception as e:
            log_error(f"Failed to load account: {str(e)}")
            return False

    def get_current_id(self):
        """Get current account ID."""
        if hasattr(self, 'current_account') and isinstance(self.current_account, dict):
            return self.current_account.get('id')
        return None

    def get_form_data(self):
        """Get current form data as dictionary"""
        try:
            timestamp = datetime.now().timestamp()
            
            data = {
                'id': self.get_current_id(),  # Use helper method
                'website': self.website_var.get().strip(),
                'username': self.username_var.get().strip(),
                'password': self.password_var.get().strip(),
                'notes': self.notes_text.get('1.0', tk.END).strip() if hasattr(self, 'notes_text') else '',
                'created_at': getattr(self, 'current_account', {}).get('created_at', timestamp),
                'modified_at': timestamp,
                'password_history': getattr(self, 'current_account', {}).get('password_history', [])
            }
            
            log_debug(f"Form data collected: {data}")
            return data
            
        except Exception as e:
            log_error(f"Failed to get form data: {str(e)}")
            return None

    def clear(self):
        """Clear form data."""
        try:
            self.current_account = {}  # Initialize as empty dict
            self.website_var.set("")
            self.username_var.set("")
            self.password_var.set("")
            if hasattr(self, 'notes_text'):
                self.notes_text.delete('1.0', tk.END)
            log_debug("Form cleared")
        except Exception as e:
            log_error(f"Failed to clear form: {str(e)}")

    def enable(self):
        """Enable form fields."""
        self.website_entry.configure(state='normal')
        self.username_entry.configure(state='normal')
        self.password_entry.configure(state='normal')

    def disable(self):
        """Disable form fields."""
        self.website_entry.configure(state='disabled')
        self.username_entry.configure(state='disabled')
        self.password_entry.configure(state='disabled')

    def validate(self):
        """Validate form data."""
        try:
            website = self.website_var.get().strip()
            username = self.username_var.get().strip()
            password = self.password_var.get()
            
            if not website:
                self.show_feedback("Website is required", "error")
                return False
            if not username:
                self.show_feedback("Username is required", "error")
                return False
            if not password:
                self.show_feedback("Password is required", "error")
                return False
            
            log_debug(f"Form validated successfully for website: {website}")
            return True
            
        except Exception as e:
            log_error(f"Validation error: {str(e)}")
            self.show_feedback("Error validating form", "error")
            return False

    def save_account(self):
        """Save current account details."""
        log_debug(f"Saving account: {self.website_var.get()}")
        try:
            website = self.website_var.get().strip()
            username = self.username_var.get().strip()
            password = self.password_var.get()
            
            # Validate inputs
            if not website or not username or not password:
                self.show_feedback("All fields are required", "error")
                return False
            
            # Save account
            if self.current_account:
                success = self.account_store.update_account(
                    self.current_account['id'],
                    website,
                    username,
                    password
                )
            else:
                success = self.account_store.add_account(
                    website,
                    username,
                    password
                )
            
            if success:
                self.show_feedback("Account saved successfully", "success")
                return True
            else:
                self.show_feedback("Error saving account", "error")
                return False
            
        except Exception as e:
            self.show_feedback(f"Save error: {str(e)}", "error")
            return False

    def is_new_account(self):
        """Check if currently adding new account."""
        return not bool(getattr(self, 'current_account', {}).get('id'))
