@echo off
echo Starting JunkBusters Website on http://localhost:8001
echo Press CTRL+C to stop.
echo.
cd /d "%~dp0"
.venv\Scripts\python manage.py runserver 8001
pause
