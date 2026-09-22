@echo off
title IIUI Streamlit Frontend
color 0E
cls
echo ============================================================
echo  IIUI Smart Chatbot - Streamlit Frontend
echo  Port: 8501
echo ============================================================
echo.
echo Make sure Flask backend is running first!
echo (Run start_flask.bat or RUN.bat)
echo.
echo Starting Streamlit...
streamlit run app.py --server.port 8501 --server.headless true
