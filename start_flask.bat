@echo off
title IIUI Flask Backend
color 0B
cls
echo ============================================================
echo  IIUI Smart Chatbot - Flask Backend
echo  Port: 5000
echo ============================================================
echo.
echo Initializing database...
python database/init_db.py >nul 2>&1
echo Starting Flask server...
echo (Model loading may take 30-60 seconds on first run)
echo.
python flask_server.py
