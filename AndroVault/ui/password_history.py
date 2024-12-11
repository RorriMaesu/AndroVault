import tkinter as tk
from tkinter import ttk
from datetime import datetime
from .tooltip import create_tooltip
from utils.error_handler import ErrorHandler
from logger import log_event, log_error

class PasswordHistory(ttk.Frame):
    def __init__(self, parent, account_manager):
        """Initialize password history widget."""
        super().__init__(parent)
        self.account_manager = account_manager
        
        self.setup_widgets()
        
    def setup_widgets(self):
        """Create the treeview for password history."""
        # Create treeview
        self.tree = ttk.Treeview(
            self,
            columns=('date', 'password'),
            show='headings'
        )
        
        # Set column headings
        self.tree.heading('date', text='Date Changed')
        self.tree.heading('password', text='Previous Password')
        
        # Configure scrollbar
        scrollbar = ttk.Scrollbar(
            self,
            orient=tk.VERTICAL,
            command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack widgets
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def update_history(self, account_id):
        """Update the history view for an account."""
        try:
            # Clear existing items
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Get password history
            history = self.account_manager.get_password_history(account_id)
            
            # Add history items
            if history:
                for entry in history:
                    masked_password = '•' * len(entry['password'])
                    self.tree.insert(
                        '',
                        'end',
                        values=(
                            datetime.fromtimestamp(entry['timestamp']).strftime('%Y-%m-%d %H:%M'),
                            masked_password
                        )
                    )

        except Exception as e:
            log_error(f"Failed to update password history: {str(e)}")
            # Use the parent's feedback mechanism instead of error handler
            if hasattr(self.master, 'show_feedback'):
                self.master.show_feedback("Failed to load password history", "error")

    def clear(self):
        """Clear the history view."""
        for item in self.tree.get_children():
            self.tree.delete(item) 