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

### 📋 Prerequisites
- Python 3.8 or higher
  - Windows users: During Python installation, **CHECK** "Add Python to PATH"
  - Verify installation by opening a terminal/command prompt and typing:
    ```bash
    python --version    # or python3 --version on Mac/Linux
    ```
  - If this doesn't work, you need to fix your Python installation first!

### ⚙️ First Time Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/AndroVault.git
   cd AndroVault
   ```

2. Create and activate a virtual environment:

   What's a virtual environment? It's like a clean room for your Python project - it keeps this project's packages separate from other Python projects on your computer.

   - On Windows (Command Prompt):
     ```bash
     # Create the virtual environment
     python -m venv venv
     
     # Activate it
     venv\Scripts\activate
     ```

   - On Mac/Linux/Git Bash:
     ```bash
     # Create the virtual environment
     python3 -m venv venv
     
     # Activate it
     source venv/bin/activate
     ```

   You'll know it worked when you see `(venv)` at the start of your terminal line!

3. Install required packages:
   ```bash
   # First, upgrade pip
   python -m pip install --upgrade pip
   
   # Then install requirements
   pip install -r requirements.txt
   ```

### 🏃‍♂️ Running the Application (After Setup)

1. Navigate to the project folder and activate the virtual environment:
   - Windows (Command Prompt):
     ```bash
     venv\Scripts\activate
     ```
   - Mac/Linux/Git Bash:
     ```bash
     source venv/bin/activate
     ```

2. Start the application:
   ```bash
   python main.py
   ```

### 🔧 Common Issues & Solutions

1. "Python not found" or "python: command not found":
   - Windows: You forgot to check "Add Python to PATH" during installation
   - Solution: Reinstall Python and CHECK the "Add Python to PATH" box
   - Or search "Edit System Environment Variables" in Windows and add Python manually

2. "pip not found":
   - Make sure you activated the virtual environment (you should see `(venv)` in your terminal)
   - Try using `python -m pip` instead of just `pip`

3. Virtual environment not working:
   - Make sure you're in the project directory
   - Try removing the `venv` folder and creating it again:
     ```bash
     # Windows
     rmdir /s /q venv
     python -m venv venv

     # Mac/Linux
     rm -rf venv
     python3 -m venv venv
     ```

4. Permission errors (Mac/Linux):
   ```bash
   # Try adding sudo
   sudo python3 -m venv venv
   ```

5. Still stuck? Make sure:
   - You're in the correct directory (where requirements.txt is)
   - Python is properly installed (try `python --version`)
   - You're using the correct commands for your operating system

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