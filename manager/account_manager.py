# manager/account_manager.py
import json
import os
from utils.password_utils import encrypt_data, decrypt_data
from logger import log_error, log_event, log_debug
from datetime import datetime
from cryptography.fernet import InvalidToken
import uuid

ACCOUNTS_FILE = "accounts.json"

class AccountManager:
    def __init__(self, master_password):
        """Initialize account manager."""
        try:
            self.master_password = master_password
            self.accounts_file = "data/accounts.enc"
            # Ensure data directory exists
            os.makedirs(os.path.dirname(self.accounts_file), exist_ok=True)
            self.accounts = self._load_accounts()
            log_event(f"AccountManager initialized with {len(self.accounts)} accounts")
        except Exception as e:
            log_error(f"Failed to initialize AccountManager: {str(e)}")
            self.accounts = []

    def get_accounts(self, search_term=None):
        """Get all accounts or filtered by search term"""
        if not search_term:
            return self.accounts
        
        search_term = search_term.lower()
        return [acc for acc in self.accounts 
                if search_term in acc.get('website', '').lower() or 
                   search_term in acc.get('username', '').lower()]

    def save_account(self, account_data):
        """Save or update an account"""
        try:
            if not account_data:
                log_error("No account data provided")
                return False
            
            log_debug(f"Attempting to save account: {account_data.get('website')}")
            
            # Ensure accounts list exists
            if not hasattr(self, 'accounts'):
                self.accounts = []
                log_debug("Initialized empty accounts list")
            
            # Validate required fields
            required_fields = ['website', 'username', 'password']
            if not all(account_data.get(field) for field in required_fields):
                log_error(f"Missing required fields: {[f for f in required_fields if not account_data.get(f)]}")
                return False

            # Generate ID for new accounts
            if not account_data.get('id'):
                account_data['id'] = str(uuid.uuid4())
                self.accounts.append(account_data)
                log_event(f"New account created with ID: {account_data['id']}")
            else:
                # Update existing account
                updated = False
                for i, acc in enumerate(self.accounts):
                    if acc['id'] == account_data['id']:
                        self.accounts[i] = account_data
                        updated = True
                        log_event(f"Updated account: {account_data['id']}")
                        break
                if not updated:
                    self.accounts.append(account_data)

            # Save to disk
            success = self._save_accounts()
            if success:
                log_event(f"Account saved successfully: {account_data.get('website')}")
                return True
            return False
            
        except Exception as e:
            log_error(f"Error saving account: {str(e)}")
            return False

    def _load_accounts(self):
        """Load accounts from encrypted file"""
        try:
            if not os.path.exists(self.accounts_file):
                log_event("No accounts file found, starting fresh")
                return []
            
            with open(self.accounts_file, 'rb') as f:
                encrypted_data = f.read()
            
            if not encrypted_data:
                log_event("Empty accounts file found")
                return []
            
            # Decrypt data
            decrypted_data = decrypt_data(encrypted_data, self.master_password)
            if not decrypted_data:
                raise ValueError("Decryption returned empty data")
            
            # Parse JSON
            accounts = json.loads(decrypted_data.decode('utf-8'))
            log_event(f"Successfully loaded {len(accounts)} accounts")
            return accounts
            
        except Exception as e:
            log_error(f"Error loading accounts: {str(e)}")
            return []

    def _save_accounts(self):
        """Encrypt and save accounts to file."""
        try:
            # Ensure data directory exists
            os.makedirs(os.path.dirname(self.accounts_file), exist_ok=True)
            
            # Convert accounts to JSON
            accounts_json = json.dumps(self.accounts)
            
            # Encrypt data
            encrypted_data = encrypt_data(accounts_json.encode(), self.master_password)
            if not encrypted_data:
                raise ValueError("Failed to encrypt accounts data")
            
            # Save to file
            with open(self.accounts_file, 'wb') as f:
                f.write(encrypted_data)
                
            log_event(f"Saved {len(self.accounts)} accounts to disk")
            return True
                
        except Exception as e:
            log_error(f"Error saving accounts file: {str(e)}")
            return False

    def get_account(self, account_id):
        """Get a single account by ID."""
        try:
            accounts = self.get_accounts()
            # Find account with matching ID
            for account in accounts:
                if account.get('id') == account_id:
                    return account
            return None
        except Exception as e:
            log_error(f"Failed to get account {account_id}: {str(e)}")
            return None

    def get_password_history(self, account_id):
        """Get password history for an account."""
        try:
            # Implementation depends on how you store password history
            # Return empty list if no history exists
            return []
        except Exception as e:
            log_error(f"Failed to get password history: {str(e)}")
            return None

    def delete_account(self, account_id):
        """Delete an account by ID."""
        try:
            if not account_id:
                log_error("No account ID provided for deletion")
                return False
            
            log_debug(f"Attempting to delete account: {account_id}")
            
            # Find account index
            for i, account in enumerate(self.accounts):
                if account.get('id') == account_id:
                    # Remove account
                    self.accounts.pop(i)
                    
                    # Save changes to disk
                    if self._save_accounts():
                        log_event(f"Account deleted successfully: {account_id}")
                        return True
                    else:
                        log_error("Failed to save changes after deletion")
                        return False
                    
            log_error(f"Account not found for deletion: {account_id}")
            return False
            
        except Exception as e:
            log_error(f"Error deleting account: {str(e)}")
            return False
