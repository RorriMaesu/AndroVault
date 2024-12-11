import tkinter as tk
from tkinter import ttk
import pyperclip
import threading
import time
from logger import log_event, log_error

class ClipboardManager:
    """Manages secure clipboard operations."""
    
    def __init__(self, feedback_widget, clear_delay=30):
        """
        Initialize clipboard manager.
        
        Args:
            feedback_widget: Widget to show feedback messages
            clear_delay: Seconds before clearing clipboard (default 30)
        """
        self.feedback = feedback_widget
        self.clear_delay = clear_delay
        self._original_clipboard = None
        self.clear_timer = None

    def copy_to_clipboard(self, text, message=None):
        """Copy text to clipboard with optional feedback message."""
        try:
            # Save current clipboard content
            self._original_clipboard = pyperclip.paste()
            
            # Copy new content
            pyperclip.copy(text)
            
            # Show feedback if message provided
            if message and self.feedback:
                self.feedback.show_message(message, "success")
            
            log_event("Text copied to clipboard")
            
            # Schedule clearing
            self._schedule_clear(text)
            return True
            
        except Exception as e:
            log_error(f"Failed to copy to clipboard: {str(e)}")
            if self.feedback:
                self.feedback.show_message("Failed to copy to clipboard", "error")
            return False

    def _schedule_clear(self, text):
        """Schedule clipboard clearing."""
        if self.clear_delay > 0:
            if self.clear_timer:
                self.clear_timer.cancel()
            self.clear_timer = threading.Timer(
                self.clear_delay,
                self._clear_clipboard,
                args=[text]
            )
            self.clear_timer.daemon = True
            self.clear_timer.start()

    def _clear_clipboard(self, text):
        """Clear clipboard if it still contains the sensitive data."""
        try:
            current = pyperclip.paste()
            if current == text:
                if self._original_clipboard:
                    pyperclip.copy(self._original_clipboard)
                else:
                    pyperclip.copy('')
                log_event("Clipboard cleared")
                if self.feedback:
                    self.feedback.show_message("Clipboard cleared", "info")
        except Exception as e:
            log_error(f"Failed to clear clipboard: {str(e)}")

    def cancel_clear(self):
        """Cancel scheduled clipboard clearing."""
        if self.clear_timer:
            self.clear_timer.cancel()
            self.clear_timer = None 