import json
import os
from logger import log_event, log_error

class SettingsManager:
    def __init__(self):
        """Initialize settings manager."""
        self.settings_file = "settings.json"
        self.default_settings = {
            "clipboard": {
                "auto_clear": True,
                "clear_delay": 30
            },
            "security": {
                "lock_timeout": 300,
                "min_password_length": 12,
                "require_special_chars": True
            },
            "backup": {
                "auto_backup": True,
                "backup_interval": 24,  # hours
                "keep_backups": 10
            },
            "ui": {
                "theme": "system",
                "font_size": 10,
                "show_password_strength": True
            }
        }
        self.settings = self._load_settings()

    def _load_settings(self):
        """Load settings from file or create default."""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    stored_settings = json.load(f)
                    # Merge with defaults to handle new settings
                    settings = self.default_settings.copy()
                    settings.update(stored_settings)
                    log_event("Settings loaded successfully")
                    return settings
            return self.default_settings.copy()
        except Exception as e:
            log_error(f"Failed to load settings: {str(e)}")
            return self.default_settings.copy()

    def save_settings(self):
        """Save current settings to file."""
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=4)
            log_event("Settings saved successfully")
            return True
        except Exception as e:
            log_error(f"Failed to save settings: {str(e)}")
            return False

    def get_setting(self, category, key):
        """Get a specific setting value."""
        try:
            return self.settings[category][key]
        except KeyError:
            return self.default_settings[category][key]

    def update_setting(self, category, key, value):
        """Update a specific setting."""
        try:
            if category not in self.settings:
                self.settings[category] = {}
            self.settings[category][key] = value
            return self.save_settings()
        except Exception as e:
            log_error(f"Failed to update setting: {str(e)}")
            return False

    def reset_to_default(self):
        """Reset all settings to default values."""
        self.settings = self.default_settings.copy()
        return self.save_settings() 