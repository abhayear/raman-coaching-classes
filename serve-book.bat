@echo off
cd /d "%~dp0book"
echo.
echo ========================================
echo  MSc Chemistry Guide
echo ========================================
echo.
echo  IMPORTANT: Do NOT use port 8080
echo  (8080 is used by PostgreSQL on your PC)
echo.
echo  Open this URL in your browser:
echo    http://localhost:8765/index.html
echo.
echo  Press Ctrl+C to stop.
echo ========================================
echo.
python -m http.server 8765
