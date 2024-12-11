# ui/search_box.py
import tkinter as tk
from tkinter import ttk
import constants
from .tooltip import create_tooltip

class SearchBox(ttk.Frame):
    def __init__(self, parent, search_callback):
        """Initialize search box."""
        super().__init__(parent)
        self.search_callback = search_callback
        self.setup_widgets()

    def setup_widgets(self):
        """Create search widgets."""
        # Search container
        search_frame = ttk.Frame(self)
        search_frame.pack(fill=tk.X)

        # Search icon (optional)
        self.search_icon = ttk.Label(
            search_frame,
            text="🔍",  # Unicode search icon
            font=constants.FONTS['default']
        )
        self.search_icon.pack(side=tk.LEFT, padx=(0, 5))

        # Search entry
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self._on_search_change)
        
        self.search_entry = ttk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=constants.FONTS['default']
        )
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        create_tooltip(self.search_entry, "Search accounts by website or username")

        # Clear button
        self.clear_button = ttk.Button(
            search_frame,
            text="✕",
            width=3,
            command=self.clear_search
        )
        self.clear_button.pack(side=tk.LEFT, padx=(5, 0))
        create_tooltip(self.clear_button, "Clear search")

        # Initially hide clear button
        self.clear_button.pack_forget()

        # Don't trigger initial search here anymore
        # self.search_callback("")  # Remove this line

    def _on_search_change(self, *args):
        """Handle search text changes."""
        search_text = self.search_var.get()
        
        # Show/hide clear button
        if search_text:
            self.clear_button.pack(side=tk.LEFT, padx=(5, 0))
        else:
            self.clear_button.pack_forget()
        
        # Call search callback
        if self.search_callback:
            self.search_callback(search_text)

    def clear_search(self):
        """Clear search field."""
        self.search_var.set("")
        self.search_entry.focus()

    def get_search_term(self):
        """Get current search term."""
        return self.search_var.get()

    def focus_search(self):
        """Focus the search entry."""
        self.search_entry.focus()
