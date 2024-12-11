from logger import log_event, log_error
from enum import Enum, auto

class AppState(Enum):
    """Application states."""
    INITIALIZING = auto()
    AUTHENTICATING = auto()
    READY = auto()
    EDITING = auto()
    SEARCHING = auto()
    LOCKED = auto()
    ERROR = auto()

class StateManager:
    def __init__(self, main_window=None):
        """Initialize state manager."""
        self.main_window = main_window
        self.current_state = AppState.INITIALIZING
        self.selected_account = None
        self.is_modified = False
        self.observers = []

    def register_observer(self, observer):
        """Register a component to receive state updates."""
        if observer not in self.observers:
            self.observers.append(observer)

    def notify_observers(self):
        """Notify all observers of state change."""
        for observer in self.observers:
            if hasattr(observer, 'on_state_change'):
                observer.on_state_change(self.current_state)

    def set_state(self, new_state, **kwargs):
        """Update application state."""
        try:
            old_state = self.current_state
            self.current_state = new_state
            
            # Log state transition
            log_event(f"State change: {old_state.name} -> {new_state.name}")
            
            # Update UI based on state
            self._handle_state_change(old_state, new_state, **kwargs)
            
            # Notify observers
            self.notify_observers()
            
        except Exception as e:
            log_error(f"Failed to change state: {str(e)}")
            self.current_state = AppState.ERROR

    def _handle_state_change(self, old_state, new_state, **kwargs):
        """Handle UI updates for state changes."""
        if not self.main_window:
            return

        if new_state == AppState.READY:
            self.main_window.enable_controls()
            self.is_modified = False
        
        elif new_state == AppState.EDITING:
            self.main_window.enable_save()
            self.is_modified = True
        
        elif new_state == AppState.LOCKED:
            self.main_window.disable_controls()
            self.selected_account = None
        
        elif new_state == AppState.SEARCHING:
            self.main_window.show_search_results(kwargs.get('results', []))

    def select_account(self, account_id):
        """Update selected account."""
        self.selected_account = account_id
        if account_id:
            self.set_state(AppState.EDITING)
        else:
            self.set_state(AppState.READY)

    def mark_modified(self):
        """Mark current state as modified."""
        if not self.is_modified:
            self.is_modified = True
            self.set_state(AppState.EDITING)

    def is_dirty(self):
        """Check if there are unsaved changes."""
        return self.is_modified

    def reset(self):
        """Reset state to initial values."""
        self.current_state = AppState.READY
        self.selected_account = None
        self.is_modified = False
        self.notify_observers() 