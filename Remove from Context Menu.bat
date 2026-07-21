@echo off
chcp 65001 > nul
echo =========================================
echo  Catbox Uploader Uninstaller (Context Menu)
echo =========================================
echo.

echo Removing registry keys...
reg delete "HKCU\Software\Classes\*\shell\UploadCatbox" /f > nul 2>&1

echo.
echo Success! The button has been completely removed from your context menu.
pause
