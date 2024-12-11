import os
import shutil
from datetime import datetime
import json
from logger import log_event, log_error

class BackupManager:
    def __init__(self, data_dir="data", backup_dir="backups"):
        """Initialize backup manager."""
        self.data_dir = data_dir
        self.backup_dir = backup_dir
        self.ensure_directories()

    def ensure_directories(self):
        """Create necessary directories if they don't exist."""
        try:
            os.makedirs(self.backup_dir, exist_ok=True)
            log_event("Backup directory initialized")
        except Exception as e:
            log_error(f"Failed to create backup directory: {str(e)}")

    def create_backup(self):
        """Create a backup of all data files."""
        try:
            # Create timestamp for backup name
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = os.path.join(self.backup_dir, f"backup_{timestamp}")
            os.makedirs(backup_path)

            # Copy data files
            files_to_backup = [
                "accounts.dat",
                "salt.key",
                "master.hash",
                "2fa.key"
            ]

            for file in files_to_backup:
                if os.path.exists(file):
                    shutil.copy2(file, backup_path)

            # Create backup info
            backup_info = {
                "timestamp": timestamp,
                "files": files_to_backup,
                "created_at": datetime.now().isoformat()
            }

            # Save backup info
            with open(os.path.join(backup_path, "backup_info.json"), 'w') as f:
                json.dump(backup_info, f, indent=4)

            log_event(f"Backup created successfully: backup_{timestamp}")
            return True

        except Exception as e:
            log_error(f"Failed to create backup: {str(e)}")
            return False

    def restore_backup(self, backup_name):
        """Restore from a specific backup."""
        try:
            backup_path = os.path.join(self.backup_dir, backup_name)
            
            # Verify backup exists
            if not os.path.exists(backup_path):
                raise FileNotFoundError("Backup not found")

            # Read backup info
            with open(os.path.join(backup_path, "backup_info.json"), 'r') as f:
                backup_info = json.load(f)

            # Restore files
            for file in backup_info["files"]:
                backup_file = os.path.join(backup_path, file)
                if os.path.exists(backup_file):
                    shutil.copy2(backup_file, file)

            log_event(f"Backup restored successfully: {backup_name}")
            return True

        except Exception as e:
            log_error(f"Failed to restore backup: {str(e)}")
            return False

    def list_backups(self):
        """List all available backups."""
        try:
            backups = []
            for backup in os.listdir(self.backup_dir):
                info_file = os.path.join(self.backup_dir, backup, "backup_info.json")
                if os.path.exists(info_file):
                    with open(info_file, 'r') as f:
                        info = json.load(f)
                        backups.append({
                            "name": backup,
                            "created_at": info["created_at"],
                            "files": info["files"]
                        })
            return backups
        except Exception as e:
            log_error(f"Failed to list backups: {str(e)}")
            return []
``` 