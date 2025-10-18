@echo off
title Erthoric Quick Install
echo ========================================
echo    Erthoric - Quick Installation
echo ========================================
echo.

echo Step 1: Checking Python...
python --version
if errorlevel 1 (
    echo ERROR: Python not found! Please install Python 3.6+
    pause
    exit /b 1
)

echo Step 2: Installing requests package...
pip install requests

echo.
echo Step 3: Launching Erthoric...
python erthoric.py

pause