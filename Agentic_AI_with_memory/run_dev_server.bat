@echo off
echo Starting Knowledge Graph Chatbot Development Server...
echo.
echo This server serves both the frontend and backend from a single process.
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

REM Start the development server
echo.
echo Starting development server...
echo Frontend: http://localhost:5000
echo API: http://localhost:5000/api
echo.
echo Press Ctrl+C to stop the server
echo.
python dev_server.py

pause