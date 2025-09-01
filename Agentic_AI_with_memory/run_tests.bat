@echo off

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

echo.
echo ========================================
echo Running Agentic AI Test Suite
echo ========================================
echo.

echo Running Memory Test...
echo ----------------------------------------
python -B src/test/memory_test.py
echo.

echo Running Cache Similarity Test...
echo ----------------------------------------
python -B src/test/test_cache_similarity.py
echo.

echo ========================================
echo All tests completed.
echo ========================================
pause 