import tkinter as tk
from datetime import datetime
from logger import log_event, log_error

class ActivityMonitor:
    def __init__(self, root, session_manager):
        """Initialize activity monitor."""
        self.root = root
        self.session_manager = session_manager
        self.last_activity = datetime.now()
        self.setup_monitors()

    def setup_monitors(self):
        """Setup event monitoring."""
        try:
            # Bind to window events
            self.root.bind_all('<Key>', self.on_activity)
            self.root.bind_all('<Motion>', self.on_activity)
            self.root.bind_all('<Button>', self.on_activity)
            self.root.bind_all('<MouseWheel>', self.on_activity)
            
            # Monitor window focus
            self.root.bind('<FocusIn>', self.on_window_focus)
            self.root.bind('<FocusOut>', self.on_window_blur)
            
            log_event("Activity monitoring initialized")
            
        except Exception as e:
            log_error(f"Failed to setup activity monitors: {str(e)}")

    def on_activity(self, event=None):
        """Handle user activity events."""
        try:
            current_time = datetime.now()
            
            # Update last activity time
            if (current_time - self.last_activity).total_seconds() > 1:
                self.last_activity = current_time
                self.session_manager.record_activity()
                
        except Exception as e:
            log_error(f"Failed to process activity: {str(e)}")

    def on_window_focus(self, event=None):
        """Handle window focus events."""
        try:
            # Record activity
            self.on_activity()
            
            # Check clipboard contents
            from ui.clipboard_manager import ClipboardManager
            if hasattr(self.root, 'clipboard_manager'):
                self.root.clipboard_manager.check_clipboard()
                
            log_event("Window focused")
            
        except Exception as e:
            log_error(f"Failed to handle window focus: {str(e)}")

    def on_window_blur(self, event=None):
        """Handle window blur events."""
        try:
            # Optional: Force clipboard clear on blur
            if hasattr(self.root, 'clipboard_manager'):
                self.root.clipboard_manager.clear_clipboard()
                
            log_event("Window blurred")
            
        except Exception as e:
            log_error(f"Failed to handle window blur: {str(e)}")

    def get_idle_time(self):
        """Get time since last activity."""
        return (datetime.now() - self.last_activity).total_seconds()

    def reset(self):
        """Reset activity monitoring."""
        self.last_activity = datetime.now()
        self.session_manager.record_activity() 