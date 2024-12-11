# ui/feedback.py
import tkinter as tk
from tkinter import ttk
from logger import log_event

class Feedback(ttk.Frame):
    def __init__(self, parent):
        """Initialize feedback widget."""
        super().__init__(parent)
        self.setup_widget()
        
    def setup_widget(self):
        """Setup the feedback label."""
        self.message_var = tk.StringVar()
        self.label = ttk.Label(
            self,
            textvariable=self.message_var,
            anchor='center',
            padding=5
        )
        self.label.pack(fill=tk.X)
        
    def show_message(self, message, message_type="info"):
        """Show a feedback message with specified type."""
        try:
            # Configure style based on message type
            if message_type == "error":
                self.label.configure(foreground='red')
            elif message_type == "success":
                self.label.configure(foreground='green')
            else:
                self.label.configure(foreground='black')
                
            # Set message
            self.message_var.set(message)
            log_event(f"Feedback shown: {message} ({message_type})")
            
        except Exception as e:
            log_error(f"Failed to show feedback: {str(e)}")
