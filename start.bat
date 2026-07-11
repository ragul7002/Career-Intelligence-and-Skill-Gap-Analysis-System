@echo off
title AI Skill Accelerator Launcher (Single IP/Port)
echo ===================================================
echo             AI SKILL ACCELERATOR LAUNCHER
echo ===================================================
echo.
echo Step 1: Building Frontend Assets...
echo.
cd frontend
call npm run build
cd ..

echo.
echo Step 2: Starting Server (Serving both API and UI on Port 5000)...
echo.
.\venv\Scripts\python backend\app.py

