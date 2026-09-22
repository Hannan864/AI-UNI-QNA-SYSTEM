@echo off
title IIUI Smart Chatbot - Test Suite
color 0F
cls
echo ============================================================
echo  IIUI Smart Chatbot - Complete Test Suite
echo ============================================================
echo.
echo Running Phase 3 tests...
python test_phase3.py 2>nul
echo.
echo Running Phase 4 tests...
python test_phase4.py 2>nul
echo.
echo Running Phase 5 tests...
python test_phase5.py 2>nul
echo.
echo Running Phase 6 tests...
python test_phase6.py 2>nul
echo.
echo Running Phase 7 tests...
python test_phase7.py 2>nul
echo.
echo Running Phase 8 tests...
python test_phase8.py 2>nul
echo.
echo Running Phase 9 tests...
python test_phase9.py 2>nul
echo.
echo Running Phase 10/11 tests...
python test_phase10_11.py 2>nul
echo.
echo ============================================================
echo  All tests complete!
echo ============================================================
echo.
pause
