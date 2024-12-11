import threading
import time
from datetime import datetime, timedelta
from logger import log_event, log_error

class SessionManager:
    def __init__(self, state_manager, settings_manager):
        """Initialize session manager."""
        self.state_manager = state_manager
        self.settings_manager = settings_manager
        self.last_activity = datetime.now()
        self.lock_timer = None
        self.is_locked = False
        
        # Start monitoring
        self.start_monitoring()

    def start_monitoring(self):
        """Start session monitoring."""
        self.lock_timer = threading.Thread(
            target=self._monitor_session,
            daemon=True
        )
        self.lock_timer.start()
        log_event("Session monitoring started")

    def _monitor_session(self):
        """Monitor session for inactivity."""
        while True:
            try:
                # Get timeout from settings
                timeout = self.settings_manager.get_setting(
                    'security',
                    'lock_timeout'
                )
                
                # Check if session should be locked
                if not self.is_locked:
                    idle_time = (datetime.now() - self.last_activity).total_seconds()
                    if idle_time > timeout:
                        self.lock_session()
                
                # Sleep for a bit
                time.sleep(1)
                
            except Exception as e:
                log_error(f"Session monitoring error: {str(e)}")
                time.sleep(5)  # Wait before retrying

    def record_activity(self):
        """Record user activity."""
        self.last_activity = datetime.now()

    def lock_session(self):
        """Lock the current session."""
        try:
            if not self.is_locked:
                self.is_locked = True
                self.state_manager.set_state(self.state_manager.AppState.LOCKED)
                log_event("Session locked due to inactivity")
        except Exception as e:
            log_error(f"Failed to lock session: {str(e)}")

    def unlock_session(self, master_password):
        """Attempt to unlock the session."""
        try:
            from auth.authentication import verify_master_password
            
            if verify_master_password(master_password):
                self.is_locked = False
                self.record_activity()
                self.state_manager.set_state(self.state_manager.AppState.READY)
                log_event("Session unlocked successfully")
                return True
            else:
                log_event("Failed unlock attempt")
                return False
                
        except Exception as e:
            log_error(f"Failed to unlock session: {str(e)}")
            return False

    def get_idle_time(self):
        """Get current idle time in seconds."""
        return (datetime.now() - self.last_activity).total_seconds()

    def get_time_until_lock(self):
        """Get seconds until session will be locked."""
        timeout = self.settings_manager.get_setting('security', 'lock_timeout')
        idle_time = self.get_idle_time()
        return max(0, timeout - idle_time)

    def force_lock(self):
        """Force an immediate session lock."""
        self.lock_session()

    def reset(self):
        """Reset session state."""
        self.record_activity()
        self.is_locked = False 