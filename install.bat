@echo off
title Erthoric Installer
echo ========================================
echo    Erthoric - Earthquake Monitor
echo          Installation Script
echo ========================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.6+ from https://python.org
    pause
    exit /b 1
)

echo Python found!
echo Installing required packages...

pip install -r requirements.txt

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo Installation completed successfully!
    echo.
    echo To run Erthoric, use: python erthoric.py
    echo ========================================
) else (
    echo.
    echo ERROR: Failed to install required packages
)

pause