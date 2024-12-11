import tkinter as tk
from tkinter import ttk
import re
from .tooltip import create_tooltip

class PasswordStrength(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.setup_widgets()

    def setup_widgets(self):
        # Progress bar for strength indicator
        self.strength_var = tk.IntVar()
        self.progress = ttk.Progressbar(
            self,
            variable=self.strength_var,
            maximum=100,
            length=150,
            mode='determinate'
        )
        self.progress.pack(side=tk.LEFT, padx=(5, 10))
        create_tooltip(self.progress, "Password strength indicator")

        # Label for strength text
        self.label_var = tk.StringVar(value="No password")
        self.label = ttk.Label(
            self,
            textvariable=self.label_var
        )
        self.label.pack(side=tk.LEFT)

    def update_strength(self, password):
        """Update the strength indicator for a password."""
        if not password:
            strength = 0
            text = "No password"
        else:
            # Calculate password strength
            strength = 0
            
            # Length contribution (up to 40%)
            length_score = min(len(password) * 4, 40)
            strength += length_score
            
            # Character variety (up to 60%)
            if re.search(r'[A-Z]', password): strength += 15
            if re.search(r'[a-z]', password): strength += 15
            if re.search(r'[0-9]', password): strength += 15
            if re.search(r'[^A-Za-z0-9]', password): strength += 15
            
            # Set description text
            if strength < 20:
                text = "Very weak"
            elif strength < 40:
                text = "Weak"
            elif strength < 60:
                text = "Moderate"
            elif strength < 80:
                text = "Strong"
            else:
                text = "Very strong"

        # Update widgets
        self.strength_var.set(strength)
        self.label_var.set(text)
        
        # Update color based on strength
        colors = {
            "Very weak": "red",
            "Weak": "orange",
            "Moderate": "yellow",
            "Strong": "light green",
            "Very strong": "green"
        }
        self.progress.configure(style=f'{colors.get(text, "grey")}.Horizontal.TProgressbar') 