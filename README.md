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

## 🚀 Installation Guide

### Step-by-Step Installation (Windows)

#### 1️⃣ Install Required Software

First, we need to install two programs that AndroVault needs to work:

**A. Install Git:**
1. Go to [git-scm.com](https://git-scm.com/downloads)
2. Click the "Windows" download button
3. When the download finishes, run the installer
4. Click "Next" for all options (default settings are fine)
5. Click "Install"
6. Click "Finish" when done

**B. Install Python:**
1. Go to [python.org](https://python.org)
2. Click "Downloads" then click "Python 3.x.x" (latest version)
3. ⚠️ VERY IMPORTANT: Check the box that says "Add Python to PATH"
4. Click "Install Now"
5. Wait for the installation to complete
6. Click "Close" when done

#### 2️⃣ Download AndroVault

Now we'll download the AndroVault program:

1. Open Command Prompt:
   - Press the Windows key + R on your keyboard
   - Type `cmd` and press Enter
   - You should see a black window with white text

2. Download AndroVault:
   - Type this command exactly as shown:
     ```bash
     git clone https://github.com/RorriMaesu/AndroVault.git
     ```
   - Press Enter
   - Wait until you see new text appear
   - You should see messages about files being downloaded

3. Go to the AndroVault folder:
   - Type this command:
     ```bash
     cd AndroVault
     ```
   - Press Enter
   - The text before the cursor should now end with '\AndroVault>'

#### 3️⃣ Install AndroVault

Now we'll run the installation script:

1. Start the installation:
   - Type this command:
     ```bash
     install.bat
     ```
   - Press Enter
   - You'll see text appearing as the installation progresses
   - This might take a few minutes
   - ✅ Success: You'll see "Installation completed successfully!"
   - ❌ If you see any errors, check the Troubleshooting section below

#### 4️⃣ Start Using AndroVault

You can start AndroVault in two ways:

**Option 1 - Using File Explorer:**
1. Open File Explorer (Windows key + E)
2. Go to where you downloaded AndroVault
3. Double-click the `launch.bat` file
4. The program should open in a new window

**Option 2 - Using Command Prompt:**
1. If you're still in Command Prompt, type:
   ```bash
   launch.bat
   ```
2. Press Enter
3. The program should open in a new window

### 🔧 Troubleshooting Common Problems

#### "Python is not recognized..."
You'll see this if Python wasn't added to PATH:
1. Uninstall Python from Windows Settings
2. Download Python again
3. ⚠️ Make sure to check "Add Python to PATH"
4. Install Python again
5. Restart your computer
6. Try the installation again

#### "Git is not recognized..."
This means Git isn't installed properly:
1. Uninstall Git
2. Download Git again
3. Install Git
4. Restart your computer
5. Try the installation again

#### Installation Errors
If the installation fails:
1. Look in the AndroVault folder for a file named `install_[numbers].log`
2. Check that your internet is working
3. Try these steps:
   - Close Command Prompt
   - Open Command Prompt as Administrator:
     - Press Windows key
     - Type "cmd"
     - Right-click "Command Prompt"
     - Click "Run as administrator"
   - Navigate back to AndroVault:
     ```bash
     cd C:\Path\To\AndroVault
     ```
   - Try installation again:
     ```bash
     install.bat
     ```

#### Still Having Problems?
1. Go to our [GitHub Issues page](https://github.com/RorriMaesu/AndroVault/issues)
2. Click "New Issue"
3. Describe what happened
4. Include the contents of your install log file
5. Our team will help you solve the problem

### ✅ How to Know Everything Worked

After installation, you should have:
1. A folder named "AndroVault" containing:
   - `launch.bat` - Used to start the program
   - `install.bat` - The installation script you used
   - Other program files and folders

When you run the program:
1. A

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