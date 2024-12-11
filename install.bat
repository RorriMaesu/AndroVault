@echo off
setlocal EnableDelayedExpansion

:: =============================================
:: AndroVault Installation Script
:: =============================================

:: Function Definitions
goto :main

:log
echo [INFO] %~1
echo [INFO] %~1 >> "%LOG_PATH%"
exit /b

:error
echo.
echo [ERROR] %~1
echo [ERROR] %~1 >> "%LOG_PATH%"
echo.
echo See "%LOG_PATH%" for details
pause
exit /b 1

:end
echo.
echo Installation log saved to: "%LOG_PATH%"
pause
exit /b 0

:main
:: Determine the script's directory
set "SCRIPT_DIR=%~dp0"

:: Change directory to the script's location
cd /d "%SCRIPT_DIR%" || (
    echo [ERROR] Failed to change directory to script location.
    exit /b 1
)

:: Define the AndroVault directory (assuming it's a subfolder)
set "ANDROVAULT_DIR=%SCRIPT_DIR%androvault"

:: Check if AndroVault directory exists
if not exist "%ANDROVAULT_DIR%\" (
    call :error "AndroVault directory not found at '%ANDROVAULT_DIR%'. Please ensure the script is placed in the correct location."
)

:: Change directory to AndroVault directory
cd /d "%ANDROVAULT_DIR%" || (
    call :error "Failed to change directory to AndroVault folder."
)

:: Verify that requirements.txt exists
if not exist "requirements.txt" (
    call :error "requirements.txt not found in AndroVault folder! Make sure you're in the correct directory."
)

:: Get current timestamp in YYYYMMDD_HHMMSS format using PowerShell
for /f %%i in ('powershell -NoProfile -Command "Get-Date -Format \"yyyyMMdd_HHmmss\""') do set "TIMESTAMP=%%i"

:: Verify that TIMESTAMP is set
if not defined TIMESTAMP (
    call :error "Failed to retrieve the current timestamp."
)

:: Initialize log file with timestamp
set "LOG_FILE=install_%TIMESTAMP%.log"
set "LOG_PATH=%ANDROVAULT_DIR%\%LOG_FILE%"

:: Start Logging
echo ============================================= > "%LOG_PATH%"
echo Installing AndroVault... >> "%LOG_PATH%"
echo Started at: %date% %time% >> "%LOG_PATH%"
echo ============================================= >> "%LOG_PATH%"

:: Begin Installation Process
call :log "Checking system requirements..."

:: Check for admin rights
net session >nul 2>&1
if %errorlevel% equ 0 (
    call :log "Running with administrator privileges."
) else (
    call :log "[WARNING] Running without administrator privileges."
    call :log "Some features may require admin rights."
    timeout /t 3 >nul
)

:: Check internet connection
call :log "Checking internet connection..."
ping 8.8.8.8 -n 1 -w 1000 >nul
if errorlevel 1 (
    call :error "No internet connection detected! Please check your connection."
)

:: Check Python installation
call :log "Checking Python installation..."
python --version >nul 2>&1
if errorlevel 1 (
    call :error "Python is not installed or not in PATH!

Please install Python 3.8 or higher:
1. Go to https://www.python.org/downloads/
2. Download Python for Windows
3. IMPORTANT: Check 'Add Python to PATH' during installation
4. Restart this installer after Python is installed."
)

:: Retrieve Python version
for /f "tokens=2 delims= " %%a in ('python --version 2^>^&1') do (
    set "PYTHON_VERSION=%%a"
    call :log "Detected Python version: %%a"
)

:: Parse version numbers
for /f "tokens=1,2 delims=." %%a in ("!PYTHON_VERSION!") do (
    set "MAJOR=%%a"
    set "MINOR=%%b"
)

:: Verify Python version
if !MAJOR! LSS 3 (
    call :error "Python 3.8 or higher is required (found version !PYTHON_VERSION!)."
)
if !MAJOR! EQU 3 if !MINOR! LSS 8 (
    call :error "Python 3.8 or higher is required (found version !PYTHON_VERSION!)."
)

:: Backup existing virtual environment if it exists
if exist venv (
    call :log "Backing up existing virtual environment..."
    set "BACKUP_NAME=venv_backup_%TIMESTAMP%"
    set "COUNTER=1"

    :: Ensure unique backup name
    :CHECK_BACKUP
    if exist "!BACKUP_NAME!" (
        set "BACKUP_NAME=venv_backup_%TIMESTAMP%_!COUNTER!"
        set /a COUNTER+=1
        goto :CHECK_BACKUP
    )

    ren venv "!BACKUP_NAME!" 2>nul
    if errorlevel 1 (
        call :error "Failed to backup existing virtual environment."
    ) else (
        call :log "Existing virtual environment backed up as !BACKUP_NAME!."
    )
)

:: Create virtual environment
call :log "Creating virtual environment..."
python -m venv venv
if errorlevel 1 call :error "Failed to create virtual environment."

:: Activate virtual environment
call :log "Activating virtual environment..."
call venv\Scripts\activate.bat
if errorlevel 1 call :error "Failed to activate virtual environment."

:: Upgrade pip
call :log "Upgrading pip..."
python -m pip install --upgrade pip >nul
if errorlevel 1 call :error "Failed to upgrade pip."

:: Install requirements
set "REQUIREMENTS_PATH=%ANDROVAULT_DIR%\requirements.txt"
if exist "%REQUIREMENTS_PATH%" (
    call :log "Installing requirements (this may take a few minutes)..."
    python -m pip install -r "%REQUIREMENTS_PATH%" || call :error "Failed to install requirements."
) else (
    call :error "requirements.txt not found in AndroVault folder! Make sure you're in the correct directory."
)

:: Finalize Installation
call :log "Installation completed successfully!"
call :log "You can now run launch.bat to start AndroVault."
goto :end
