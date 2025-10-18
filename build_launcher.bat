@echo off
title Building Erthoric Launcher
echo ========================================
echo    Building Erthoric Launcher EXE
echo ========================================
echo.

echo Installing PyInstaller if not exists...
pip install pyinstaller

echo.
echo Building launcher executable...
pyinstaller --onefile --windowed --icon=erthoric_icon.ico --name ErthoricLauncher ErthoricLauncher.py

if exist "dist\ErthoricLauncher.exe" (
    echo.
    echo ========================================
    echo Build completed successfully!
    echo Launcher: dist\ErthoricLauncher.exe
    echo ========================================
) else (
    echo.
    echo ERROR: Build failed!
)

pause