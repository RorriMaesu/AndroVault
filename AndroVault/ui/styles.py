import tkinter as tk
from tkinter import ttk
import platform

class AppStyle:
    # Modern color palette
    COLORS = {
        'primary': '#2557a7',      # Main brand color
        'primary_dark': '#1a4380', # Darker shade
        'secondary': '#6c757d',    # Secondary elements
        'success': '#28a745',      # Success messages
        'warning': '#ffc107',      # Warning messages
        'danger': '#dc3545',       # Error/danger messages
        'background': '#f8f9fa',   # Main background
        'surface': '#ffffff',      # Card/surface background
        'text': '#212529',         # Main text color
        'text_secondary': '#6c757d' # Secondary text
    }

    # Modern styling
    def apply(self):
        style = ttk.Style()
        
        # Configure main styles
        style.configure('Main.TFrame', background=self.COLORS['background'])
        style.configure('Surface.TFrame', background=self.COLORS['surface'])
        
        # Modern button styles
        style.configure('Primary.TButton',
            background=self.COLORS['primary'],
            foreground='white',
            padding=(20, 10),
            font=('Segoe UI', 10)
        )
        
        # List view style
        style.configure('AccountList.Treeview',
            background=self.COLORS['surface'],
            fieldbackground=self.COLORS['surface'],
            font=('Segoe UI', 10),
            rowheight=30
        )
        
        # Entry fields
        style.configure('Modern.TEntry',
            padding=10,
            fieldbackground=self.COLORS['surface']
        )

        # Custom progressbar styles for password strength
        for color in ['red', 'orange', 'yellow', 'light green', 'green']:
            style.configure(
                f'{color}.Horizontal.TProgressbar',
                background=color,
                troughcolor=self.COLORS['background']
            ) 

def apply_component_style(widget, style_name):
    """Apply predefined style to widget"""
    if style_name in constants.COMPONENT_STYLES:
        widget.configure(**constants.COMPONENT_STYLES[style_name]) 

def apply_button_style(button, style_type='default'):
    """Apply consistent button styling"""
    button.configure(
        padding=constants.PADDING['medium'],
        font=constants.FONTS['default']
    )