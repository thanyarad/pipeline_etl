@echo off
echo Opening Knowledge Graph Chatbot Frontend...
echo.

REM Get the current directory
set "CURRENT_DIR=%~dp0"

REM Open the frontend HTML file in the default browser
start "" "%CURRENT_DIR%frontend\index.html"

echo Frontend opened in your default browser.
echo Make sure the backend server is running on http://localhost:5000
echo.
pause
