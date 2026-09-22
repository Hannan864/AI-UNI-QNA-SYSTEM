@echo off
title IIUI Smart Chatbot - Stop
color 0C
cls
echo ============================================================
echo  IIUI Smart Chatbot - Stopping Application
echo ============================================================
echo.

echo Stopping Flask Backend (port 5000)...
for /f "tokens=5" %%a in ('netstat -aon 2^>nul ^| findstr ":5000" ^| findstr "LISTENING"') do (
    echo   Killing process %%a on port 5000
    taskkill /F /PID %%a >nul 2>&1
)
echo [OK] Flask stopped.

echo.
echo Stopping Streamlit Frontend (port 8501)...
for /f "tokens=5" %%a in ('netstat -aon 2^>nul ^| findstr ":8501" ^| findstr "LISTENING"') do (
    echo   Killing process %%a on port 8501
    taskkill /F /PID %%a >nul 2>&1
)
echo [OK] Streamlit stopped.

echo.
echo ============================================================
echo  Application stopped successfully.
echo ============================================================
echo.
pause
