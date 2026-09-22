@echo off
title IIUI Smart Chatbot - System Check
color 0F
cls
echo ============================================================
echo  IIUI Smart Chatbot - System Health Check
echo ============================================================
echo.

set "PASS=0"
set "FAIL=0"

REM === Check Python ===
echo [1] Python
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo     PASS - Python available
    set /a "PASS+=1"
) else (
    echo     FAIL - Python not found!
    set /a "FAIL+=1"
)

REM === Check Flask ===
echo [2] Flask dependency
python -c "import flask" >nul 2>&1
if %errorlevel% equ 0 (
    echo     PASS - Flask installed
    set /a "PASS+=1"
) else (
    echo     FAIL - Flask not installed
    set /a "FAIL+=1"
)

REM === Check Streamlit ===
echo [3] Streamlit dependency
python -c "import streamlit" >nul 2>&1
if %errorlevel% equ 0 (
    echo     PASS - Streamlit installed
    set /a "PASS+=1"
) else (
    echo     FAIL - Streamlit not installed
    set /a "FAIL+=1"
)

REM === Check NLTK ===
echo [4] NLTK dependency
python -c "import nltk" >nul 2>&1
if %errorlevel% equ 0 (
    echo     PASS - NLTK installed
    set /a "PASS+=1"
) else (
    echo     FAIL - NLTK not installed
    set /a "FAIL+=1"
)

REM === Check spaCy ===
echo [5] spaCy dependency
python -c "import spacy" >nul 2>&1
if %errorlevel% equ 0 (
    echo     PASS - spaCy installed
    set /a "PASS+=1"
) else (
    echo     FAIL - spaCy not installed
    set /a "FAIL+=1"
)

REM === Check scikit-learn ===
echo [6] Scikit-learn dependency
python -c "import sklearn" >nul 2>&1
if %errorlevel% equ 0 (
    echo     PASS - Scikit-learn installed
    set /a "PASS+=1"
) else (
    echo     FAIL - Scikit-learn not installed
    set /a "FAIL+=1"
)

REM === Check Database ===
echo [7] Database file
if exist "database\iiui_data.db" (
    echo     PASS - Database exists
    set /a "PASS+=1"
) else (
    echo     FAIL - Database file not found
    set /a "FAIL+=1"
)

REM === Check Flask Backend ===
echo [8] Flask Backend (port 5000)
curl -s http://localhost:5000/api/health 2>nul | findstr "healthy" >nul 2>&1
if %errorlevel% equ 0 (
    echo     PASS - Flask Backend running and healthy
    set /a "PASS+=1"
) else (
    echo     FAIL - Flask Backend not responding
    set /a "FAIL+=1"
)

REM === Check Streamlit Frontend ===
echo [9] Streamlit Frontend (port 8501)
curl -s -o nul -w "%%{http_code}" http://localhost:8501 2>nul | findstr "200" >nul 2>&1
if %errorlevel% equ 0 (
    echo     PASS - Streamlit Frontend running
    set /a "PASS+=1"
) else (
    echo     FAIL - Streamlit Frontend not responding
    set /a "FAIL+=1"
)

REM === Check key files ===
echo [10] Project files
if exist "app.py" if exist "flask_server.py" if exist "config.py" if exist "requirements.txt" (
    echo     PASS - Core files present
    set /a "PASS+=1"
) else (
    echo     FAIL - Some core files missing
    set /a "FAIL+=1"
)

REM === Summary ===
echo.
echo ============================================================
echo  RESULTS: %PASS% passed, %FAIL% failed out of 10 checks
echo ============================================================
echo.

if %FAIL% equ 0 (
    echo  All checks passed! Application is ready.
) else (
    echo  Some checks failed. Review above for issues.
)
echo.
pause
