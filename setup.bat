@echo off
echo ========================================
echo QR Menu - Quick Setup Script
echo ========================================
echo.

echo [1/7] Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)
echo ✓ Virtual environment created
echo.

echo [2/7] Activating virtual environment...
call venv\Scripts\activate.bat
echo ✓ Virtual environment activated
echo.

echo [3/7] Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo ✓ Dependencies installed
echo.

echo [4/7] Running migrations...
python manage.py makemigrations
python manage.py migrate
if %errorlevel% neq 0 (
    echo ERROR: Failed to run migrations
    pause
    exit /b 1
)
echo ✓ Database created
echo.

echo [5/7] Populating sample data...
python manage.py populate_sample_data
if %errorlevel% neq 0 (
    echo ERROR: Failed to populate sample data
    pause
    exit /b 1
)
echo ✓ Sample data loaded
echo.

echo [6/7] Generating QR codes...
python manage.py generate_qr_codes
if %errorlevel% neq 0 (
    echo ERROR: Failed to generate QR codes
    pause
    exit /b 1
)
echo ✓ QR codes generated
echo.

echo [7/7] Collecting static files...
python manage.py collectstatic --noinput
echo ✓ Static files collected
echo.

echo ========================================
echo ✓ Setup completed successfully!
echo ========================================
echo.
echo Default credentials:
echo   Admin:   admin / admin123
echo   Kitchen: kitchen / kitchen123
echo   Waiter:  waiter / waiter123
echo.
echo To start the server, run:
echo   python manage.py runserver
echo.
echo Then open: http://localhost:8000
echo.
pause
