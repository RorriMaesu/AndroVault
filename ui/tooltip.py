# ui/tooltip.py
import tkinter as tk
from tkinter import ttk

class ToolTip:
    def __init__(self, widget, text):
        """Initialize tooltip."""
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind('<Enter>', self.show)
        self.widget.bind('<Leave>', self.hide)

    def show(self, event=None):
        """Display tooltip."""
        try:
            # Get widget position
            x = self.widget.winfo_rootx()
            y = self.widget.winfo_rooty() + self.widget.winfo_height()
            
            # Create tooltip window
            self.tooltip = tk.Toplevel(self.widget)
            self.tooltip.wm_overrideredirect(True)
            self.tooltip.wm_geometry(f"+{x}+{y}")
            
            label = tk.Label(self.tooltip, text=self.text, 
                           justify=tk.LEFT, background="#ffffe0", 
                           relief=tk.SOLID, borderwidth=1)
            label.pack()
            
        except Exception as e:
            log_error(f"Tooltip error: {str(e)}")

    def hide(self, event=None):
        """Hide tooltip."""
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

def create_tooltip(widget, text):
    """Create a tooltip for a widget."""
    return ToolTip(widget, text)
