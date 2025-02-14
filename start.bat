@echo off
SETLOCAL

REM Check if Python is installed
where python >nul 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Please install Python 3.
    exit /b 1
)

REM Create virtual environment if it doesn't exist
IF NOT EXIST venv (
    python -m venv venv
)

REM Activate virtual environment
CALL venv\Scripts\activate

REM Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

REM Start Flask app
python app.py
