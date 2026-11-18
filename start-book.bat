@echo off
cd /d "%~dp0"
echo Starting book server on port 8765...
start "MSc Chemistry Book Server" cmd /k "%~dp0serve-book.bat"
timeout /t 2 /nobreak >nul
start "" "http://localhost:8765/index.html"
echo.
echo Browser opened. If it fails, wait 3 seconds and open:
echo   http://localhost:8765/index.html
pause
