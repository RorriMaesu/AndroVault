@echo off
setlocal

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH!
    echo Please install Python and try again.
    pause
    exit /b 1
)

:: Check if we're in the correct directory by looking for requirements.txt
if not exist "requirements.txt" (
    echo Error: requirements.txt not found!
    echo Please run this script from the AndroVault project root directory
    echo (The directory containing requirements.txt)
    pause
    exit /b 1
)

echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Upgrading pip...
python -m pip install --upgrade pip

echo Installing requirements...
pip install -r requirements.txt

echo.
echo Setup complete! Your virtual environment is ready.
echo To activate the virtual environment in the future, run: venv\Scripts\activate.bat
echo.

pause