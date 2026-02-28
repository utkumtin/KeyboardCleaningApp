@echo off
:: Keyboard Cleaning App — Run with Administrator privileges
:: Check if already running as admin
net session >nul 2>&1
if %errorlevel% neq 0 (
    powershell -Command "Start-Process '%~f0' -Verb RunAs -WindowStyle Hidden"
    exit /b
)

cd /d "%~dp0"
start "" /b pythonw -m src.main
exit
