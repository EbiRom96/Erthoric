@echo off
title Building Erthoric EXE
chcp 65001 >nul
echo ========================================
echo    Building Erthoric Executable
echo ========================================
echo.

echo Step 1: Installing PyInstaller...
pip install pyinstaller

echo.
echo Step 2: Building executable...
pyinstaller --onefile --console --name "Erthoric" --icon=erthoric_icon.ico erthoric.py

if exist "dist\Erthoric.exe" (
    echo.
    echo ========================================
    echo ✅ Build completed successfully!
    echo 📁 Executable: dist\Erthoric.exe
    echo ========================================
    echo.
    echo You can now distribute Erthoric.exe
    echo It includes Python and all dependencies!
) else (
    echo.
    echo ❌ Build failed!
)

echo.
pause