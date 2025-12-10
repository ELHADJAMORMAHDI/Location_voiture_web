#!/bin/bash

# Django Car Rental Setup Script for Linux/Mac

echo "================================"
echo "Location Voiture - Django Setup"
echo "================================"
echo ""

# Create virtual environment
echo "[1/6] Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "[2/6] Installing dependencies..."
pip install -r requirements.txt

# Create .env file
echo "[3/6] Creating .env file..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env file - please update with your settings"
fi

# Run migrations
echo "[4/6] Running migrations..."
python manage.py migrate

# Create superuser
echo "[5/6] Creating superuser..."
python manage.py createsuperuser

# Collect static files
echo "[6/6] Collecting static files..."
python manage.py collectstatic --noinput

echo ""
echo "================================"
echo "Setup Complete!"
echo "================================"
echo ""
echo "To start the server:"
echo "  source venv/bin/activate"
echo "  python manage.py runserver"
echo ""
echo "Admin panel: http://localhost:8000/admin/"
