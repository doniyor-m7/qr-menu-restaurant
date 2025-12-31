@echo off
echo Starting QR Menu server...
echo.

call venv\Scripts\activate.bat

python manage.py runserver

pause
