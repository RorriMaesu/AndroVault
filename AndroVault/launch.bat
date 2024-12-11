@echo off
cd %~dp0AndroVault
call venv\Scripts\activate.bat
python main.py
deactivate
cd .. 