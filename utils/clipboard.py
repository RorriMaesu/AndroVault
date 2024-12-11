# utils/clipboard.py
import tkinter as tk
import pyperclip
from logger import log_event, log_error
import threading
import time

def copy_to_clipboard(text, clear_after=30):
    """
    Copy text to clipboard and optionally clear after specified seconds.
    
    Args:
        text (str): Text to copy
        clear_after (int): Seconds after which to clear clipboard (0 to disable)
    """
    try:
        # Copy to clipboard
        pyperclip.copy(text)
        log_event("Text copied to clipboard")
        
        # Schedule clipboard clearing if enabled
        if clear_after > 0:
            def clear_clipboard():
                time.sleep(clear_after)
                if pyperclip.paste() == text:
                    pyperclip.copy('')
                    log_event("Clipboard cleared for security")
            
            # Run in background thread
            threading.Thread(
                target=clear_clipboard,
                daemon=True
            ).start()
            
        return True
        
    except Exception as e:
        log_error(f"Failed to copy to clipboard: {str(e)}")
        return False
