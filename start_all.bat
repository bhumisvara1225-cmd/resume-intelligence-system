@echo off
title TalentIQ Resume Intelligence System
color 0A

echo ============================================
echo   TalentIQ Resume Intelligence System
echo ============================================
echo.

:: ── Kill any stale processes on our ports ───────────────────────
echo [1/4] Cleaning up old processes...

for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8080 " ^| findstr "LISTENING"') do (
    echo      Killing old backend process (PID %%a)...
    taskkill /PID %%a /F >nul 2>&1
)

for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":5173 " ^| findstr "LISTENING"') do (
    echo      Killing old frontend process (PID %%a)...
    taskkill /PID %%a /F >nul 2>&1
)

timeout /t 1 /nobreak >nul

:: ── Check venv exists ────────────────────────────────────────────
echo [2/4] Checking virtual environment...
if not exist "venv\Scripts\activate.bat" (
    echo      ERROR: venv not found! Run: python -m venv venv ^&^& venv\Scripts\activate ^&^& pip install -r requirements.txt
    pause
    exit /b 1
)
echo      venv found OK.

:: ── Check node_modules ──────────────────────────────────────────
echo [3/4] Checking frontend dependencies...
if not exist "frontend\node_modules" (
    echo      node_modules not found. Installing...
    cd frontend
    call npm install
    cd ..
)
echo      node_modules OK.

:: ── Start both servers ──────────────────────────────────────────
echo [4/4] Starting servers...
echo.

start "TalentIQ Backend (port 8080)" cmd /k "title TalentIQ Backend && color 0B && echo Starting FastAPI backend... && venv\Scripts\activate && uvicorn app.main:app --reload --port 8080"

timeout /t 2 /nobreak >nul

start "TalentIQ Frontend (port 5173)" cmd /k "title TalentIQ Frontend && color 0D && echo Starting Vite frontend... && cd frontend && npm run dev"

echo.
echo ============================================
echo   Both servers starting in new windows!
echo ============================================
echo.
echo   Frontend  -->  http://localhost:5173
echo   Backend   -->  http://localhost:8080
echo   API Docs  -->  http://localhost:8080/docs
echo.
echo   Wait 5 seconds then open your browser.
echo ============================================
echo.
timeout /t 5 /nobreak >nul
start "" "http://localhost:5173"
