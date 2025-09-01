@echo off
echo Starting Knowledge Graph Chatbot Application...
echo.
echo This will start the backend server and open the frontend in your browser.
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

REM Start the backend server in the background
echo.
echo Starting Flask backend server on http://localhost:5000
echo.
start /B python backend/app.py

REM Wait a moment for the server to start
timeout /t 3 /nobreak >nul

REM Open the frontend in the default browser
echo Opening frontend in your default browser...
start "" "http://localhost:5000"

echo.
echo Application started successfully!
echo - Backend server: http://localhost:5000
echo - Frontend: Opened in your browser
echo.
echo Press any key to stop the backend server...
pause

REM Stop the backend server
taskkill /f /im python.exe >nul 2>&1
echo Backend server stopped.
pause
