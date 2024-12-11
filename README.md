<div align="center">
  <img src="logo.png" alt="Password Manager Logo" width="200">
</div>

# 🔐 Password Manager

A secure, feature-rich password management application built with Python and Tkinter.

## 📁 Project Structure
```
.
├── 2fa.key
├── README.md
├── app.log
├── auth/
│   ├── __init__.py
│   ├── authentication.py
│   ├── two_factor.py
│   ├── utils.py
├── constants.py
├── data/
│   ├── account_store.py
│   ├── accounts.enc
│   ├── backup_manager.py
│   ├── settings_manager.py
├── list_structure.py
├── logger.py
├── logs/
├── main.py
├── manager/
│   ├── __init__.py
│   ├── account_manager.py
├── master.hash
├── requirements.txt
├── ui/
│   ├── __init__.py
│   ├── account_detail.py
│   ├── account_list.py
│   ├── action_buttons.py
│   ├── clipboard_manager.py
│   ├── feedback.py
│   ├── login_window.py
│   ├── main_window.py
│   ├── password_generator.py
│   ├── password_history.py
│   ├── password_strength.py
│   ├── search_box.py
│   ├── styles.py
│   ├── tooltip.py
└── utils/
    ├── __init__.py
    ├── activity_monitor.py
    ├── clipboard.py
    ├── crypto.py
    ├── error_handler.py
    ├── password_utils.py
    ├── session_manager.py
    └── state_manager.py
```

## 🏗️ Technical Architecture

### 🔑 1. Authentication Layer (`auth/`)

**authentication.py**
- Implements multi-factor authentication flow
- Manages master password verification
- Coordinates with 2FA system
- Handles first-time setup and subsequent logins

**two_factor.py**
```python:auth/two_factor.py
startLine: 187
endLine: 275
```
- TOTP-based two-factor authentication
- QR code generation for authenticator apps
- Secure secret storage with encryption
- Verification flow with retry logic

**utils.py**
- Cryptographic primitives for authentication
- Password hashing using industry standards
- Key derivation functions
- Secure random generation

### 💾 2. Data Management Layer (`data/`)

**account_store.py**
- Implements encrypted data persistence
- AES-256 encryption for stored data
- CRUD operations for account data
- Search and filtering capabilities

**backup_manager.py**
- Automated backup scheduling
- Encrypted backup creation
- Version control for backups
- Recovery procedures

**settings_manager.py**
- Application configuration management
- Security settings control
- User preferences storage
- Default value handling

### 🖥️ 3. User Interface Layer (`ui/`)

**main_window.py**
- Central UI orchestration
- Component lifecycle management
- Event handling and routing
- State synchronization

**Components:**
- `account_detail.py`: Account form with validation
- `account_list.py`: Filterable account display
- `password_generator.py`: Cryptographically secure generation
- `password_strength.py`: Real-time strength evaluation
- `clipboard_manager.py`: Secure copy operations

### 🛠️ 4. Utility Layer (`utils/`)

**Security Utilities:**
- `crypto.py`: Encryption operations
- `password_utils.py`: Password handling
- `session_manager.py`: Session security
- `activity_monitor.py`: Auto-lock system

**Application Utilities:**
- `state_manager.py`: Application state machine
- `error_handler.py`: Error management
- `clipboard.py`: Safe clipboard operations

## 🔒 Security Implementation

### 🔐 Authentication Chain
1. Master Password Verification
   - Argon2 password hashing
   - Secure key derivation
   - Salt management

2. Two-Factor Authentication
   - TOTP implementation
   - Encrypted secret storage
   - QR code generation

3. Session Management
   - Activity monitoring
   - Auto-lock functionality
   - Secure state management

### 🛡️ Data Protection
1. Storage Security
   - AES-256 encryption
   - Secure key management
   - Protected memory handling

2. Runtime Security
   - Clipboard protection
   - Memory clearing
   - Session isolation

## 📋 Development Guidelines

### ⚡ Security Requirements
1. Authentication
   - Implement rate limiting
   - Enforce strong passwords
   - Require 2FA setup

2. Data Handling
   - Always encrypt sensitive data
   - Clear memory after use
   - Validate all inputs

3. Session Security
   - Monitor user activity
   - Implement timeouts
   - Secure state management

### ✨ Best Practices
1. Code Organization
   - Follow component structure
   - Maintain separation of concerns
   - Document security features

2. Error Handling
   - Comprehensive logging
   - Secure error messages
   - Graceful degradation

3. Testing
   - Security test cases
   - Integration testing
   - UI/UX validation

## 🚀 Getting Started

### 📋 Step 1: Install Python

You'll need Python 3.8 or higher installed on your computer.

**Windows Users**:
1. Go to [python.org](https://python.org)
2. Click "Downloads" and download the latest Python version
3. Run the installer
4. ⚠️ IMPORTANT: Check the box that says "Add Python to PATH"
5. Click "Install Now"

**Mac Users**:
- Option 1 (Recommended):
  1. Go to [brew.sh](https://brew.sh)
  2. Copy and paste the installation command into Terminal
  3. Run: `brew install python3`
- Option 2:
  1. Go to [python.org](https://python.org)
  2. Download the Mac installer
  3. Double-click and follow the instructions

**Linux Users**:
Open Terminal and run:
- Ubuntu/Debian: `sudo apt install python3`
- Fedora: `sudo dnf install python3`

### ⚙️ Step 2: Install AndroVault

1. Clone the repository or download ZIP:
   ```bash
   git clone https://github.com/yourusername/AndroVault.git
   ```
   Or use the green "Code" button to download ZIP

2. If you downloaded ZIP:
   - Extract it to a location you'll remember
   - Open the extracted folder

3. Run the installation script:

   **Windows Users**:
   - Double-click `install.bat`
   - Or open Command Prompt and run:
     ```cmd
     install.bat
     ```

   **Mac/Linux Users**:
   - Open Terminal and run:
     ```bash
     chmod +x install.sh
     ./install.sh
     ```

### 🏃‍♂️ Step 3: Running AndroVault

**Windows Users**:
- Double-click `launch.bat`
- Or open Command Prompt and run:
  ```cmd
  launch.bat
  ```

**Mac/Linux Users**:
- Open Terminal and run:
  ```bash
  chmod +x launch.sh
  ./launch.sh
  ```

### 🔧 Troubleshooting

**Windows Problems:**
1. "Python is not recognized..."
   - ✅ Go back to Step 1 and reinstall Python
   - ✅ Make sure you checked "Add Python to PATH"

2. "Windows protected your PC" message
   - ✅ Click "More info"
   - ✅ Click "Run anyway"

**Mac/Linux Problems:**
1. "Permission denied"
   - ✅ Run: `chmod +x install.sh launch.sh`

2. Can't find Python
   - ✅ Mac: Run `brew install python3`
   - ✅ Ubuntu/Debian: Run `sudo apt install python3`

**Still Stuck?**
1. Make sure you're in the folder containing `install.bat`/`install.sh`
2. Try restarting your computer
3. [Open an issue](https://github.com/yourusername/AndroVault/issues) on our GitHub page

## 📖 File Descriptions

### Authentication System
- `authentication.py`: Handles user authentication through master password and 2FA
- `two_factor.py`: Implements TOTP-based two-factor authentication
- `utils.py`: Provides cryptographic and authentication utilities

### Data Management
- `account_store.py`: Manages encrypted storage of account data
- `backup_manager.py`: Handles automated backups and recovery
- `settings_manager.py`: Manages application configuration

### User Interface
- `main_window.py`: Orchestrates UI components and user interaction
- `account_detail.py`: Provides account viewing and editing interface
- `password_generator.py`: Implements secure password generation
- `clipboard_manager.py`: Manages secure clipboard operations

### Utilities
- `activity_monitor.py`: Tracks user activity for security
- `crypto.py`: Provides encryption and decryption operations
- `session_manager.py`: Manages user sessions and timeouts
- `state_manager.py`: Handles application state transitions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

[MIT License](LICENSE)