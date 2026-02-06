@echo off
REM Quick Start Script for Household Spending App (Windows)

echo ======================================
echo Household Spending Estimates - Quick Start
echo ======================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo X Python is not installed. Please install Python 3.11 or higher.
    pause
    exit /b 1
)

echo [OK] Python found
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo [OK] Virtual environment created
) else (
    echo [OK] Virtual environment exists
)

REM Activate virtual environment
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo.
echo Installing dependencies...
pip install -q -r requirements.txt
echo [OK] Dependencies installed

REM Run the application
echo.
echo Starting Flask application...
echo.
echo    Dashboard: http://localhost:5000
echo    Press Ctrl+C to stop
echo.
python app.py

pause
