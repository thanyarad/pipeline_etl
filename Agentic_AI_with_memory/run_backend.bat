@echo off
echo Starting Knowledge Graph Chatbot Backend...
echo.

REM Check if virtual environment exists, if not create one
if not exist ".venv\Scripts\activate.bat" (
    echo Virtual environment not found. Creating one...
    python -m venv .venv
    if errorlevel 1 (
        echo Error: Failed to create virtual environment. Please check Python installation.
        pause
        exit /b 1
    )
)

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Install requirements if needed
echo Installing requirements...
python -m pip install --upgrade pip >nul
python -m pip install -r requirements.txt

REM Start the backend server
echo.
echo Starting Flask backend server on http://localhost:5000
echo Press Ctrl+C to stop the server
echo.
python backend/app.py

pause
