import traceback
from logger import log_error
from tkinter import messagebox

class ErrorHandler:
    def __init__(self, feedback_widget=None):
        """Initialize error handler."""
        self.feedback = feedback_widget

    def handle_error(self, error, context="", show_message=True):
        """Handle an error with logging and user feedback."""
        # Get full error details
        error_type = type(error).__name__
        error_message = str(error)
        stack_trace = traceback.format_exc()

        # Log the error
        log_error(f"{context}: {error_type} - {error_message}")
        log_error(f"Stack trace:\n{stack_trace}")

        # User-friendly messages
        friendly_messages = {
            "FileNotFoundError": "Required file not found.",
            "PermissionError": "Access denied. Check permissions.",
            "ValueError": "Invalid value provided.",
            "KeyError": "Required data not found.",
            "CryptoError": "Encryption/decryption failed.",
            "ConnectionError": "Network connection failed.",
        }

        # Get user-friendly message
        user_message = friendly_messages.get(
            error_type,
            "An unexpected error occurred."
        )

        # Show error to user
        if show_message:
            if self.feedback:
                self.feedback.show_message(
                    f"Error: {user_message}",
                    "error"
                )
            else:
                messagebox.showerror(
                    "Error",
                    f"{user_message}\n\n{error_message}"
                )

        return False

    def wrap_error(self, func):
        """Decorator to wrap functions with error handling."""
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                return self.handle_error(
                    e,
                    context=f"Error in {func.__name__}"
                )
        return wrapper

    @staticmethod
    def format_error(error):
        """Format error for display."""
        return f"{type(error).__name__}: {str(error)}" 