@echo off
echo Starting Knowledge Graph Chatbot Backend...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Install requirements if needed
echo Installing requirements...
pip install -r requirements.txt

REM Start the backend server
echo.
echo Starting Flask backend server on http://localhost:5000
echo Press Ctrl+C to stop the server
echo.
python backend/app.py

pause
