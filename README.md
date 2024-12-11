
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
├── utils/
│   ├── __init__.py
│   ├── activity_monitor.py
│   ├── clipboard.py
│   ├── crypto.py
│   ├── error_handler.py
│   ├── password_utils.py
│   ├── session_manager.py
│   ├── state_manager.py


# Password Manager

A secure, feature-rich password management application built with Python and Tkinter.

## Technical Architecture

### 1. Authentication Layer (`auth/`)

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

### 2. Data Management Layer (`data/`)

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

### 3. User Interface Layer (`ui/`)

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

### 4. Utility Layer (`utils/`)

**Security Utilities:**
- `crypto.py`: Encryption operations
- `password_utils.py`: Password handling
- `session_manager.py`: Session security
- `activity_monitor.py`: Auto-lock system

**Application Utilities:**
- `state_manager.py`: Application state machine
- `error_handler.py`: Error management
- `clipboard.py`: Safe clipboard operations

## Security Implementation

### Authentication Chain
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

### Data Protection
1. Storage Security
   - AES-256 encryption
   - Secure key management
   - Protected memory handling

2. Runtime Security
   - Clipboard protection
   - Memory clearing
   - Session isolation

## Development Guidelines

### Security Requirements
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

### Best Practices
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

## Project Structure

### Root Directory
- `main.py` - Application entry point, initializes core components and UI
- `constants.py` - Global constants and configuration settings
- `logger.py` - Centralized logging configuration and utilities
- `requirements.txt` - Project dependencies
- `list_structure.py` - Utility to display project structure
- `2fa.key` - Encrypted two-factor authentication secrets
- `master.hash` - Hashed master password storage
- `app.log` - Application log file

### Authentication (`auth/`)
- `authentication.py` - Core authentication logic and master password verification
- `two_factor.py` - Two-factor authentication implementation using TOTP
- `utils.py` - Authentication-related utility functions

### Data Management (`data/`)
- `account_store.py` - Core encrypted storage implementation
- `accounts.enc` - Encrypted account data file
- `backup_manager.py` - Automated backup and restore functionality
- `settings_manager.py` - Application settings management

### Account Management (`manager/`)
- `account_manager.py` - Business logic for account operations

### User Interface (`ui/`)
- `main_window.py` - Main application window and component orchestration
- `login_window.py` - Authentication interface
- `account_detail.py` - Account viewing and editing form
- `account_list.py` - Account listing and selection interface
- `action_buttons.py` - UI action controls (add, save, delete)
- `clipboard_manager.py` - Secure clipboard operations
- `feedback.py` - User feedback system
- `password_generator.py` - Secure password generation tool
- `password_history.py` - Password version tracking
- `password_strength.py` - Password strength evaluation
- `search_box.py` - Account search functionality
- `styles.py` - UI styling configuration
- `tooltip.py` - Tooltip component

### Utilities (`utils/`)
- `activity_monitor.py` - User activity tracking for auto-lock
- `clipboard.py` - Low-level clipboard operations
- `crypto.py` - Cryptographic operations
- `error_handler.py` - Centralized error handling
- `password_utils.py` - Password-related utilities
- `session_manager.py` - Session management and timeout handling
- `state_manager.py` - Application state management

## Security Features

1. **Authentication**
   - Master password protection
   - Two-factor authentication (TOTP)
   - Session management with auto-lock

2. **Data Protection**
   - AES-256 encryption for stored data
   - Secure password generation
   - Password strength evaluation
   - Automatic clipboard clearing

3. **Session Security**
   - Activity monitoring
   - Automatic session timeout
   - Secure memory handling

## Core Workflows

1. **Authentication Flow**
   - Master password verification
   - 2FA setup/verification
   - Session initialization

2. **Account Management**
   - Secure account storage
   - Password history tracking
   - Search and filtering
   - Backup and recovery

3. **Security Operations**
   - Encryption/decryption of data
   - Secure clipboard handling
   - Password generation
   - Activity monitoring

## Development

### Prerequisites
```bash
python -m pip install -r requirements.txt
```

### Running the Application
```bash
python main.py
```

### Security Considerations
- All sensitive data is encrypted at rest
- Memory is cleared after use
- Clipboard contents are automatically cleared
- Session timeouts enforce security
- Password strength requirements enforced

## File Descriptions

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

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[MIT License](LICENSE)