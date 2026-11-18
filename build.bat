@echo off
cd /d "%~dp0"
echo Building MSc Chemistry Guide...
python scripts\build_curriculum.py
python scripts\generate_book.py
where mdbook >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
  echo mdBook not found — building with Python HTML exporter...
  pip install markdown -q
  python scripts\build_html.py
) else (
  mdbook build
)
echo.
echo Done! Open book\index.html in your browser.
echo To save as PDF: Ctrl+P -^> Save as PDF
pause
