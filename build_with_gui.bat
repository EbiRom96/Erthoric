@echo off
title Build EXE with GUI
echo ========================================
echo    Building EXE with Auto PY to EXE
echo ========================================
echo.

echo Step 1: Installing Auto PY to EXE...
pip install auto-py-to-exe

echo.
echo Step 2: Launching GUI...
auto-py-to-exe

echo.
echo Follow these settings in the GUI:
echo - Script Location: Select erthoric.py
echo - Onefile: ☑ Yes
echo - Console Window: ☑ Console Based
echo - Icon: Select erthoric_icon.ico
echo - Additional Files: Add all .txt and .md files
echo - Then click "CONVERT .PY TO .EXE"
echo.
pause