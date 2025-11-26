@echo off
title DweepLingo Translation App

echo Starting DweepLingo...
cd /d %~dp0
cd server

start "DweepLingo Server" cmd /c "python app.py"
timeout /t 5 /nobreak >nul
start http://127.0.0.1:8000

echo.
echo Browser opened! Server is running in another window.
pause