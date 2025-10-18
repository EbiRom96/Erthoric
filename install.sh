#!/bin/bash

echo "========================================"
echo "   Erthoric - Earthquake Monitor"
echo "         Installation Script"
echo "========================================"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 is not installed"
    echo "Please install Python 3.6+ from your package manager"
    exit 1
fi

echo "Python3 found: $(python3 --version)"
echo "Installing required packages..."

# Install requirements
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo
    echo "========================================"
    echo "Installation completed successfully!"
    echo
    echo "To run Erthoric, use: python3 erthoric.py"
    echo "========================================"
else
    echo
    echo "ERROR: Failed to install required packages"
    exit 1
fi