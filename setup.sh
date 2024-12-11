#!/bin/bash

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python is not installed!"
    echo "Please install Python and try again."
    exit 1
fi

# Check if we're in the correct directory
if [ ! -f "requirements.txt" ]; then
    echo "Error: requirements.txt not found!"
    echo "Please run this script from the AndroVault project root directory"
    echo "(The directory containing requirements.txt)"
    exit 1
fi

echo "Creating virtual environment..."
python3 -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

echo "Upgrading pip..."
python -m pip install --upgrade pip

echo "Installing requirements..."
pip install -r requirements.txt

echo
echo "Setup complete! Your virtual environment is ready."
echo "To activate the virtual environment in the future, run: source venv/bin/activate"
echo

read -p "Press Enter to continue..."