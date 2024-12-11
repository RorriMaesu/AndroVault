# ui/action_buttons.py
import tkinter as tk
from tkinter import ttk
from .tooltip import create_tooltip
from logger import log_event, log_error, log_debug
import constants

class ActionButtons(ttk.Frame):
    def __init__(self, parent, add_callback, save_callback, delete_callback):
        super().__init__(parent)
        self.add_callback = add_callback
        self.save_callback = save_callback
        self.delete_callback = delete_callback
        self.setup_widgets()

    def setup_widgets(self):
        """Create action buttons."""
        # Add Account button - Prepares form for new account
        self.add_button = ttk.Button(
            self,
            text="New Account",
            command=lambda: self.handle_add()
        )
        self.add_button.pack(side=tk.LEFT, padx=(0, 10))

        # Save Changes button - Saves current form data
        self.save_button = ttk.Button(
            self,
            text="Save Account",
            command=lambda: self.handle_save(),
            state='disabled'
        )
        self.save_button.pack(side=tk.LEFT, padx=(0, 10))

        # Delete Account button
        self.delete_button = ttk.Button(
            self,
            text="Delete Account",
            command=lambda: self.handle_delete(),
            state='disabled'
        )
        self.delete_button.pack(side=tk.LEFT)

    def handle_add(self):
        """Handle add button click - Prepares new account form."""
        log_debug("New Account button clicked")
        if self.add_callback:
            self.add_callback()
            self.enable_save()
            self.disable_delete()

    def handle_save(self):
        """Handle save button click - Saves current form data."""
        log_debug("Save Account button clicked")
        if self.save_callback:
            if self.save_callback():
                self.disable_save()

    def enable_save(self):
        """Enable the save button."""
        self.save_button.config(state='normal')
        self.enable_delete()

    def disable_save(self):
        """Disable the save button."""
        self.save_button.config(state='disabled')

    def handle_delete(self):
        """Handle delete button click - Deletes current account."""
        log_debug("Delete Account button clicked")
        if self.delete_callback:
            if self.delete_callback():
                self.disable_save()
                self.disable_delete()

    def enable_delete(self):
        """Enable the delete button."""
        self.delete_button.config(state='normal')

    def disable_delete(self):
        """Disable the delete button."""
        self.delete_button.config(state='disabled')
