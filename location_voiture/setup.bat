@echo off
REM Django Car Rental Setup Script for Windows

echo ================================
echo Location Voiture - Django Setup
echo ================================
echo.

REM Create virtual environment
echo [1/6] Creating virtual environment...
python -m venv venv
call venv\Scripts\activate.bat

REM Install dependencies
echo [2/6] Installing dependencies...
pip install -r requirements.txt

REM Create .env file
echo [3/6] Creating .env file...
if not exist .env (
    copy .env.example .env
    echo Created .env file - please update with your settings
)

REM Run migrations
echo [4/6] Running migrations...
python manage.py migrate

REM Create superuser
echo [5/6] Creating superuser...
python manage.py createsuperuser

REM Collect static files
echo [6/6] Collecting static files...
python manage.py collectstatic --noinput

echo.
echo ================================
echo Setup Complete!
echo ================================
echo.
echo To start the server:
echo   venv\Scripts\activate.bat
echo   python manage.py runserver
echo.
echo Admin panel: http://localhost:8000/admin/
