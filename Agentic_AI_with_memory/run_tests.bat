@echo off
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