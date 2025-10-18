@echo off
title Create Icon for Erthoric
echo Creating icon file...

:: Create a simple icon using PowerShell
powershell -Command "
Add-Type -AssemblyName System.Drawing
`$bitmap = New-Object System.Drawing.Bitmap 64, 64
`$graphics = [System.Drawing.Graphics]::FromImage(`$bitmap)
`$graphics.Clear([System.Drawing.Color]::FromArgb(30, 144, 255))
`$font = New-Object System.Drawing.Font('Arial', 16, [System.Drawing.FontStyle]::Bold)
`$brush = [System.Drawing.Brushes]::White
`$graphics.DrawString('E', `$font, `$brush, 22, 20)
`$graphics.Dispose()
`$bitmap.Save('erthoric_icon.ico', [System.Drawing.Imaging.ImageFormat]::Icon)
"

if exist "erthoric_icon.ico" (
    echo ✅ Icon created successfully: erthoric_icon.ico
) else (
    echo ❌ Failed to create icon
    echo Please download an icon manually and name it 'erthoric_icon.ico'
)

pause