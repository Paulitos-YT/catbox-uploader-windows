@echo off
chcp 65001 > nul
echo =========================================
echo  Catbox Uploader Installer (Context Menu)
echo =========================================
echo.

set "EXE_PATH=%~dp0catbox_uploader.exe"

if not exist "%EXE_PATH%" (
    echo ERROR: The file "catbox_uploader.exe" was not found in the current folder.
    echo Make sure this installer is in the same folder as the application.
    echo.
    pause
    exit /b
)

echo Adding registry keys...
reg add "HKCU\Software\Classes\*\shell\UploadCatbox" /ve /d "Upload to Catbox" /f > nul
reg add "HKCU\Software\Classes\*\shell\UploadCatbox" /v "Icon" /d "\"%EXE_PATH%\"" /f > nul
reg add "HKCU\Software\Classes\*\shell\UploadCatbox\command" /ve /d "\"%EXE_PATH%\" \"%%1\"" /f > nul

echo.
echo Success! The "Upload to Catbox" button has been added to your right-click menu.
pause
