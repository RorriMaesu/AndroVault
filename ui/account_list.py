# ui/account_list.py
import tkinter as tk
from tkinter import ttk
import constants
from .tooltip import create_tooltip
from logger import log_event, log_error, log_debug

class AccountList(ttk.Frame):
    def __init__(self, parent, select_callback):
        """Initialize account list."""
        super().__init__(parent)
        self.select_callback = select_callback
        self.setup_widgets()

    def setup_widgets(self):
        """Create list widgets."""
        # List container with scrollbar
        list_frame = ttk.Frame(self)
        list_frame.pack(fill=tk.BOTH, expand=True)

        # Create treeview
        self.tree = ttk.Treeview(
            list_frame,
            columns=('website', 'username'),
            show='headings',
            selectmode='browse'
        )

        # Configure columns
        self.tree.heading('website', text='Website')
        self.tree.heading('username', text='Username')
        
        self.tree.column('website', width=150, minwidth=100)
        self.tree.column('username', width=150, minwidth=100)

        # Add scrollbars
        y_scroll = ttk.Scrollbar(
            list_frame,
            orient=tk.VERTICAL,
            command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=y_scroll.set)

        # Pack widgets
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        y_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Bind selection event
        self.tree.bind('<<TreeviewSelect>>', self._on_select)
        
        # Add tooltips
        create_tooltip(self.tree, "Double-click to edit account")

    def update_accounts(self, accounts):
        """Update the account list."""
        try:
            # Store current selection
            current_selection = self.tree.selection()
            
            # Clear existing items
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Add new items
            for account in accounts:
                self.tree.insert(
                    '',
                    'end',
                    iid=account['id'],
                    values=(
                        account['website'],
                        account['username']
                    )
                )

            # Restore selection if it still exists
            if current_selection and current_selection[0] in self.tree.get_children():
                self.tree.selection_set(current_selection)

            log_event(f"Account list updated with {len(accounts)} items")

        except Exception as e:
            log_error(f"Failed to update account list: {str(e)}")

    def _on_select(self, event):
        """Handle account selection."""
        selection = self.tree.selection()
        if selection and self.select_callback:
            account_id = selection[0]
            log_debug(f"Account selected from list: {account_id}")
            self.select_callback(account_id)

    def get_selected(self):
        """Get selected account ID."""
        selection = self.tree.selection()
        return selection[0] if selection else None

    def clear_selection(self):
        """Clear current selection."""
        self.tree.selection_remove(self.tree.selection())

    def select_account(self, account_id):
        """Select specific account."""
        try:
            if account_id in self.tree.get_children():
                self.tree.selection_set(account_id)
                self.tree.see(account_id)  # Ensure visible
                # Important: Trigger the selection callback
                self.select_callback(account_id)
                log_debug(f"Selected account: {account_id}")
        except Exception as e:
            log_error(f"Failed to select account: {str(e)}")
