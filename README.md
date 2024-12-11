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
   - Memory protection

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

### 📋 Prerequisites
- Python 3.8 or higher (Make sure Python is added to your PATH during installation)
- Git (for cloning the repository)

### ⚙️ Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/AndroVault.git
   cd AndroVault
   ```

2. Run the setup script:
   - On Windows:
     - Double-click `setup.bat`, or
     - Run in Command Prompt:
     ```bash
     setup.bat
     ```
     - Or using Git Bash:
     ```bash
     ./setup.sh
     ```
   
   - On Unix/Linux/Mac:
     ```bash
     chmod +x setup.sh  # Make script executable (first time only)
     ./setup.sh
     ```

   This will:
   - Create a virtual environment
   - Install all required dependencies
   - Set up the initial configuration

### 🏃‍♂️ Running the Application
1. Activate the virtual environment (if not already activated):
   - Windows Command Prompt:
     ```bash
     venv\Scripts\activate
     ```
   - Git Bash/Unix/Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

2. Start the application:
   ```bash
   python main.py
   ```

### 🔧 Troubleshooting

1. **Python not found**:
   - Ensure Python is installed and added to PATH
   - Windows users: Check "Add Python to PATH" during installation
   - Verify by running `python --version` or `python3 --version`

2. **Permission Issues** (Unix/Linux/Mac):
   - Make setup script executable: `chmod +x setup.sh`
   - Run with sudo if needed: `sudo ./setup.sh`

3. **Virtual Environment Issues**:
   - If `venv` creation fails, try:
     ```bash
     python -m pip install --upgrade virtualenv
     python -m virtualenv venv
     ```

4. **Requirements Installation Fails**:
   - Try upgrading pip first:
     ```bash
     python -m pip install --upgrade pip
     ```
   - Install requirements individually if needed:
     ```bash
     pip install pyperclip bcrypt cryptography pyotp qrcode Pillow
     ```

### 🔐 Security Considerations
- All sensitive data is encrypted at rest
- Memory is cleared after use
- Clipboard contents are automatically cleared
- Session timeouts enforce security
- Password strength requirements enforced

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