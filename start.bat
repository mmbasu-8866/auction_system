@echo off
REM Advanced Auction System - Quick Start Script for Windows

echo ======================================
echo   Advanced Online Auction System
echo ======================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo Found: %PYTHON_VERSION%
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo Dependencies installed successfully
echo.

echo ======================================
echo   Starting Auction Server...
echo ======================================
echo.
echo Server will be accessible at:
echo    Local:    http://localhost:5000
echo    External: http//:^<YOUR_IP^>:5000
echo.
echo Press Ctrl+C to stop the server
echo.

REM Run the server
python web_server.py

pause
