import json
import os
from datetime import datetime
from cryptography.fernet import Fernet
from logger import log_event, log_error

class AccountStore:
    def __init__(self, master_password):
        """Initialize account storage with encryption."""
        self.cipher = Fernet(self._derive_key(master_password))
        self.data_file = "accounts.dat"
        self.accounts = self._load_accounts()

    def _derive_key(self, master_password):
        """Derive encryption key from master password."""
        import base64
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
        
        # Use stored salt or generate new one
        salt_file = "salt.key"
        if os.path.exists(salt_file):
            with open(salt_file, 'rb') as f:
                salt = f.read()
        else:
            salt = os.urandom(16)
            with open(salt_file, 'wb') as f:
                f.write(salt)

        # Derive key using PBKDF2
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
        return key

    def _load_accounts(self):
        """Load and decrypt accounts from file."""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'rb') as f:
                    encrypted_data = f.read()
                    decrypted_data = self.cipher.decrypt(encrypted_data)
                    accounts = json.loads(decrypted_data.decode())
                    log_event("Accounts loaded successfully")
                    return accounts
            return []
        except Exception as e:
            log_error(f"Failed to load accounts: {str(e)}")
            return []

    def save_accounts(self):
        """Encrypt and save accounts to file."""
        try:
            encrypted_data = self.cipher.encrypt(
                json.dumps(self.accounts).encode()
            )
            with open(self.data_file, 'wb') as f:
                f.write(encrypted_data)
            log_event("Accounts saved successfully")
            return True
        except Exception as e:
            log_error(f"Failed to save accounts: {str(e)}")
            return False

    def add_account(self, website, username, password):
        """Add a new account."""
        account = {
            'id': self._generate_id(),
            'website': website,
            'username': username,
            'password': password,
            'created_at': datetime.now().timestamp(),
            'modified_at': datetime.now().timestamp(),
            'password_history': []
        }
        self.accounts.append(account)
        return self.save_accounts()

    def update_account(self, account_id, website, username, password):
        """Update an existing account."""
        for account in self.accounts:
            if account['id'] == account_id:
                # Store old password in history
                if account['password'] != password:
                    account['password_history'].append({
                        'password': account['password'],
                        'timestamp': datetime.now().timestamp()
                    })
                # Update account
                account['website'] = website
                account['username'] = username
                account['password'] = password
                account['modified_at'] = datetime.now().timestamp()
                return self.save_accounts()
        return False

    def _generate_id(self):
        """Generate a unique account ID."""
        import uuid
        return str(uuid.uuid4())

    def get_accounts(self, search_term=None):
        """Get all accounts, optionally filtered by search term."""
        if not search_term:
            return self.accounts
            
        search_term = search_term.lower()
        return [
            acc for acc in self.accounts
            if search_term in acc['website'].lower() or 
               search_term in acc['username'].lower()
        ]

    def get_account(self, account_id):
        """Get a specific account by ID."""
        for account in self.accounts:
            if account['id'] == account_id:
                return account
        return None 