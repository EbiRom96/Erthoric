@echo off
title Building Erthoric Installer
echo ========================================
echo    Building Erthoric Installer
echo ========================================
echo.

echo Checking for Inno Setup...
where iscc >nul 2>&1

if %errorlevel% neq 0 (
    echo ERROR: Inno Setup is not installed or not in PATH
    echo.
    echo Please install Inno Setup from:
    echo https://jrsoftware.org/isdl.php
    echo.
    pause
    exit /b 1
)

echo Building launcher first...
call build_launcher.bat

echo.
echo Copying files to setup directory...
if not exist "SetupFiles" mkdir "SetupFiles"
copy "erthoric.py" "SetupFiles\"
copy "README.md" "SetupFiles\"
copy "Donation.txt" "SetupFiles\"
copy "requirements.txt" "SetupFiles\"
copy "erthoric_icon.ico" "SetupFiles\"
copy "dist\ErthoricLauncher.exe" "SetupFiles\"
copy "LICENSE" "SetupFiles\"

echo.
echo Building installer with Inno Setup...
iscc setup.iss

if exist "Output\Erthoric_Setup.exe" (
    echo.
    echo ========================================
    echo Installer built successfully!
    echo Installer: Output\Erthoric_Setup.exe
    echo ========================================
) else (
    echo.
    echo ERROR: Installer build failed!
)

echo.
echo Cleaning up...
if exist "SetupFiles" rmdir /s /q "SetupFiles"
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "ErthoricLauncher.spec" del "ErthoricLauncher.spec"

pause