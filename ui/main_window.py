# ui/main_window.py
import tkinter as tk
from tkinter import ttk
from .account_detail import AccountDetail
from .search_box import SearchBox
from .account_list import AccountList
from .action_buttons import ActionButtons
from .feedback import Feedback
from .password_generator import PasswordGenerator
from logger import log_event, log_error, log_debug
import constants
import uuid
from datetime import datetime
from tkinter import messagebox
from .clipboard_manager import ClipboardManager

class MainWindow(ttk.Frame):
    def __init__(self, root, account_manager):
        """Initialize main window."""
        try:
            super().__init__(root)
            self.root = root
            self.account_store = account_manager
            
            # Initialize components to None first
            self.account_list = None
            self.search_box = None
            self.account_detail = None
            self.actions = None
            self.feedback = None
            
            # Initialize feedback first
            self.feedback = Feedback(self.root)
            self.feedback.pack(fill=tk.X, pady=5)
            
            # Initialize clipboard manager with feedback
            self.clipboard_manager = ClipboardManager(self.feedback)
            
            # Configure window
            self.setup_window()
            self.setup_styles()
            self.create_widgets()
            
            # Now that everything is initialized, load accounts
            self.refresh_accounts()
            
            log_event("Main window initialized successfully")
            
        except Exception as e:
            log_error(f"Failed to initialize main window: {str(e)}")
            raise

    def setup_window(self):
        """Configure the main window."""
        self.root.title("AndroVault Password Manager")
        self.root.geometry("1024x768")
        self.root.minsize(800, 600)
        self.pack(fill=tk.BOTH, expand=True)

    def setup_styles(self):
        """Setup ttk styles."""
        style = ttk.Style()
        style.configure('Accent.TButton', padding=5)
        style.configure('Feedback.TLabel', padding=10)

    def create_widgets(self):
        """Create and setup all window widgets."""
        try:
            log_debug("Creating main window widgets")
            
            # Create main container
            main_container = ttk.Frame(self)
            main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Left panel for search and list
            left_panel = ttk.Frame(main_container)
            left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
            # Create feedback widget first
            self.feedback = Feedback(left_panel)
            self.feedback.pack(fill=tk.X, pady=(0, 10))
            
            # Create search box before account list
            self.search_box = SearchBox(left_panel, self.on_search)
            self.search_box.pack(fill=tk.X, pady=(0, 10))
            
            # Create account list after search box
            self.account_list = AccountList(left_panel, self.on_account_select)
            self.account_list.pack(fill=tk.BOTH, expand=True)

            # Right panel
            right_panel = ttk.Frame(main_container)
            right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

            # Account detail with feedback callback
            self.account_detail = AccountDetail(
                right_panel,
                self.account_store,
                self.show_feedback,
                self.clipboard_manager
            )
            self.account_detail.pack(fill=tk.BOTH, expand=True)

            # Action buttons
            self.actions = ActionButtons(
                right_panel,
                self.on_add_account,
                self.on_save_changes,
                self.on_delete_account
            )
            self.actions.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))

            # Initialize clipboard manager with feedback widget
            self.clipboard_manager = ClipboardManager(self.feedback)
            
            # Pass clipboard manager to password generator
            self.password_generator = PasswordGenerator(
                right_panel,
                self.on_password_generated,
                self.clipboard_manager
            )

        except Exception as e:
            log_error(f"Failed to create widgets: {str(e)}")
            raise

    def on_search(self, search_term):
        """Handle search."""
        try:
            results = self.account_store.get_accounts(search_term)
            self.account_list.update_accounts(results)
        except Exception as e:
            log_error(f"Search error: {str(e)}")
            self.show_feedback("Search failed", "error")

    def on_account_select(self, account_id):
        """Handle account selection."""
        try:
            if not account_id:
                return
            
            log_debug(f"Loading account: {account_id}")
            account = self.account_store.get_account(account_id)
            
            if account:
                self.account_detail.load_account(account)
                self.actions.enable_save()  # Enable save button for editing
                log_event(f"Account loaded: {account_id}")
            else:
                log_error(f"Account not found: {account_id}")
            
        except Exception as e:
            log_error(f"Failed to load account: {str(e)}")

    def on_add_account(self):
        """Create and add new account immediately."""
        try:
            log_debug("New Account button clicked - Creating new account")
            
            # Get current form data
            if not self.account_detail.validate():
                log_error("Account validation failed")
                return False
            
            account_data = self.account_detail.get_form_data()
            if not account_data:
                log_error("Failed to get form data")
                self.show_feedback("Error getting form data", "error")
                return False
            
            # Create new account
            account_data['id'] = str(uuid.uuid4())
            account_data['created_at'] = datetime.now().timestamp()
            account_data['modified_at'] = account_data['created_at']
            
            # Save to store
            if self.account_store.save_account(account_data):
                self.show_feedback("New account added", "success")
                self.refresh_accounts()
                # Select the new account
                self.account_list.select_account(account_data['id'])
                log_event(f"New account added: {account_data.get('website')}")
                return True
            else:
                self.show_feedback("Failed to add account", "error")
                return False
            
        except Exception as e:
            log_error(f"Failed to add new account: {str(e)}")
            self.show_feedback("Failed to add account", "error")
            return False

    def on_save_changes(self):
        """Update existing account only."""
        try:
            log_debug("Save changes triggered")
            
            # Get current account ID
            current_id = self.account_detail.get_current_id()
            if not current_id:
                self.show_feedback("No account selected to update", "error")
                return False
            
            if not self.account_detail.validate():
                log_error("Account validation failed")
                return False
            
            account_data = self.account_detail.get_form_data()
            if not account_data:
                log_error("Failed to get form data")
                self.show_feedback("Error getting form data", "error")
                return False
            
            # Ensure we're updating existing account
            account_data['modified_at'] = datetime.now().timestamp()
            
            # Save changes
            if self.account_store.save_account(account_data):
                self.show_feedback("Account updated successfully", "success")
                self.refresh_accounts()
                return True
            else:
                self.show_feedback("Failed to update account", "error")
                return False
            
        except Exception as e:
            log_error(f"Save error: {str(e)}")
            self.show_feedback("Error updating account", "error")
            return False

    def on_delete_account(self):
        """Delete the currently selected account."""
        try:
            # Get current account ID
            current_id = self.account_detail.get_current_id()
            if not current_id:
                self.show_feedback("No account selected to delete", "error")
                return False
            
            # Confirm deletion
            if not messagebox.askyesno(
                "Confirm Delete",
                "Are you sure you want to delete this account?\nThis action cannot be undone."
            ):
                return False
            
            # Delete the account
            if self.account_store.delete_account(current_id):
                self.show_feedback("Account deleted successfully", "success")
                self.refresh_accounts()
                # Clear the form
                self.account_detail.clear()
                return True
            else:
                self.show_feedback("Failed to delete account", "error")
                return False
            
        except Exception as e:
            log_error(f"Delete error: {str(e)}")
            self.show_feedback("Error deleting account", "error")
            return False

    def show_feedback(self, message, message_type="info"):
        """Show feedback message."""
        self.feedback.show_message(message, message_type)

    def refresh_accounts(self):
        """Refresh the accounts list."""
        try:
            log_debug("Refreshing account list")
            accounts = self.account_store.get_accounts()
            
            if accounts is not None:
                self.account_list.update_accounts(accounts)
                log_event(f"Account list updated with {len(accounts)} items")
            else:
                log_error("Failed to get accounts from store")
                self.show_feedback("Failed to refresh accounts", "error")
            
        except Exception as e:
            log_error(f"Failed to refresh accounts: {str(e)}")
            self.show_feedback("Failed to refresh accounts", "error")

    def on_password_generated(self, password):
        """Handle generated password."""
        try:
            # Update password field
            self.account_detail.set_password(password)
            log_event("Password generated and applied")
        except Exception as e:
            log_error(f"Failed to handle generated password: {str(e)}")
