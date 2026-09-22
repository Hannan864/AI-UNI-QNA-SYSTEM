@echo off
setlocal enabledelayedexpansion
title IIUI Smart Chatbot - One Click Launcher
color 0A
cls

REM === Determine project root from this script's location ===
set "PROJECT_DIR=%~dp0"
cd /d "%PROJECT_DIR%"

echo ============================================================
echo     IIUI SMART CHATBOT - ONE CLICK LAUNCHER
echo     AI Chatbot for University Support
echo ============================================================
echo.

REM === Check Python ===
echo [1/8] Checking Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [FAIL] Python is not installed or not in PATH!
    echo        Download from https://www.python.org/downloads/
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('python --version 2^>^&1') do echo [OK] %%i
echo.

REM === Check if ports already in use ===
echo [2/8] Checking ports...
netstat -an 2>nul | findstr ":5000 " | findstr "LISTENING" >nul 2>&1
if %errorlevel% equ 0 (
    echo [INFO] Port 5000 already in use. Flask may already be running.
    set "FLASK_RUNNING=1"
) else (
    set "FLASK_RUNNING=0"
)

netstat -an 2>nul | findstr ":8501 " | findstr "LISTENING" >nul 2>&1
if %errorlevel% equ 0 (
    echo [INFO] Port 8501 already in use. Streamlit may already be running.
    set "ST_RUNNING=1"
) else (
    set "ST_RUNNING=0"
)
echo.

REM === Check dependencies ===
echo [3/8] Checking dependencies...
python -c "import flask" >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Installing dependencies...
    pip install -r requirements.txt -q
    if %errorlevel% neq 0 (
        echo [FAIL] Failed to install dependencies!
        pause
        exit /b 1
    )
)
echo [OK] Dependencies ready.
echo.

REM === Initialize database ===
echo [4/8] Initializing database...
python database/init_db.py >nul 2>&1
echo [OK] Database ready.
echo.

REM === Start Flask Backend ===
echo [5/8] Starting Flask Backend...
if "%FLASK_RUNNING%"=="0" (
    start "IIUI Flask Backend" cmd /k "cd /d \"%PROJECT_DIR%\" && title IIUI Flask Backend [Port 5000] && color 0B && echo Starting Flask Backend... && python flask_server.py"
    echo [INFO] Flask starting in new window...
) else (
    echo [OK] Flask already running.
)
echo.

REM === Wait for Flask health ===
echo [6/8] Waiting for Flask health check...
if "%FLASK_RUNNING%"=="0" (
    set /a "attempts=0"
    :wait_flask
    set /a "attempts+=1"
    if !attempts! geq 60 (
        echo [WARN] Flask health check timed out after 180s. Check the Flask window.
        goto flask_done
    )
    timeout /t 3 /nobreak >nul
    curl -s http://localhost:5000/api/health 2>nul | findstr "healthy" >nul 2>&1
    if %errorlevel% equ 0 (
        echo [OK] Flask Backend is HEALTHY!
        goto flask_done
    )
    if !attempts! equ 5 echo [INFO] Still loading models... (first run takes ~60s)
    if !attempts! equ 15 echo [INFO] Still loading...
    if !attempts! equ 30 echo [INFO] Still waiting...
    goto wait_flask
    :flask_done
) else (
    echo [OK] Skipped (already running).
)
echo.

REM === Start Streamlit Frontend ===
echo [7/8] Starting Streamlit Frontend...
if "%ST_RUNNING%"=="0" (
    start "IIUI Streamlit Frontend" cmd /k "cd /d \"%PROJECT_DIR%\" && title IIUI Streamlit Frontend [Port 8501] && color 0E && echo Starting Streamlit Frontend... && streamlit run app.py --server.port 8501 --server.headless true"
    echo [INFO] Streamlit starting in new window...
    timeout /t 10 /nobreak >nul
) else (
    echo [OK] Streamlit already running.
)
echo.

REM === Open Browser ===
echo [8/8] Opening browser...
timeout /t 3 /nobreak >nul
start "" "http://localhost:8501"

echo.
echo ============================================================
echo     APPLICATION STATUS
echo ============================================================
echo.
echo     Flask Backend:   http://localhost:5000
echo     Streamlit UI:    http://localhost:8501
echo.
echo     Default Admin Login:
echo       Email:    admin@iiu.edu.pk
echo       Password: admin123
echo.
echo     To register a new student account:
echo       Click "Create Account" on the login page.
echo.
echo ============================================================
echo     Both servers are running in separate windows.
echo     Close those windows to stop the application.
echo ============================================================
echo.
echo Press any key to close this launcher...
pause >nul
