# Django Car Rental Project - Location Voiture

## Overview
This is a complete Django-based car rental web application that integrates with Odoo ERP backend. It provides a customer-facing website for browsing available cars, making reservations, and managing bookings, along with a REST API for integration with mobile apps.

## Project Structure

```
location_voiture/
├── manage.py                          # Django management script
├── requirements.txt                   # Python dependencies
├── README.md                          # This file
├── .env                               # Environment variables (create this)
│
├── location_voiture/                  # Main Django project
│   ├── __init__.py
│   ├── settings.py                    # Django settings
│   ├── urls.py                        # Main URL configuration
│   ├── asgi.py                        # ASGI config
│   └── wsgi.py                        # WSGI config
│
├── cars/                              # Cars app (main features)
│   ├── migrations/
│   ├── templates/cars/
│   │   ├── car_list.html             # Browse cars
│   │   ├── car_detail.html           # View car details
│   │   ├── booking_form.html         # Create booking
│   │   ├── booking_confirmation.html # Confirm booking
│   │   ├── my_bookings.html          # View user bookings
│   │   └── dashboard.html            # User dashboard
│   ├── static/css/                    # CSS files
│   ├── static/js/                     # JavaScript files
│   ├── models.py                      # Car, Booking, Customer models
│   ├── views.py                       # Regular views
│   ├── views_api.py                   # DRF API views
│   ├── serializers.py                 # DRF serializers
│   ├── forms.py                       # Django forms
│   ├── urls.py                        # App URL patterns
│   ├── urls_api.py                    # API URL patterns
│   ├── admin.py                       # Admin configuration
│   └── apps.py                        # App config
│
├── accounts/                          # User accounts & auth
│   ├── migrations/
│   ├── templates/accounts/
│   │   ├── login.html                # Login page
│   │   ├── signup.html               # Registration page
│   │   ├── profile.html              # View profile
│   │   └── profile_setup.html        # Profile completion
│   ├── models.py                      # UserProfile model
│   ├── views.py                       # Auth views
│   ├── forms.py                       # Auth forms
│   ├── urls.py                        # Auth URL patterns
│   ├── admin.py                       # Admin config
│   └── apps.py                        # App config
│
├── odoo_integration/                  # Odoo ERP integration
│   ├── __init__.py
│   ├── odoo_connector.py             # Main Odoo connector (XML-RPC & REST)
│   ├── sync_manager.py               # Sync logic between Django & Odoo
│   └── example_usage.py              # Usage examples
│
└── templates/                         # Base templates
    ├── base.html                     # Base template
    └── home.html                     # Home page
```

## Features

### Customer-Facing Features
- **Browse Cars**: View available cars with filters (fuel type, transmission, price)
- **Car Details**: Detailed information about each car
- **Booking System**: Easy-to-use reservation system with date/time selection
- **User Authentication**: Sign up, login, logout
- **Profile Management**: Complete and edit customer profiles
- **Booking History**: View all bookings and cancel if needed
- **Dashboard**: Personal dashboard with statistics and active bookings

### Admin Features
- **Django Admin**: Manage cars, bookings, customers, availability
- **Admin Actions**: Confirm/cancel bookings in bulk
- **Reporting**: View booking statistics and customer information

### API Features (REST Framework)
- **Car API**: List and filter cars, get details
- **Booking API**: Create, update, cancel bookings
- **Authentication**: Session-based authentication

### Odoo Integration
- **Fetch Cars**: Synchronize vehicles from Odoo fleet module
- **Create Bookings**: Send booking data to Odoo
- **Manage Customers**: Sync customer information to Odoo
- **Bidirectional Sync**: Keep Django and Odoo in sync
- **XML-RPC & REST API**: Support for both communication protocols

## Installation & Setup

### 1. Prerequisites
- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)

### 2. Create Virtual Environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the project root:
```env
DEBUG=True
SECRET_KEY=your-secret-key-here-change-in-production
DATABASE_URL=sqlite:///db.sqlite3

# Odoo Configuration
ODOO_BASE_URL=http://localhost:8069
ODOO_DATABASE=odoo_db
ODOO_USERNAME=admin
ODOO_PASSWORD=admin
ODOO_USE_XMLRPC=True
```

### 5. Initialize Database
```bash
python manage.py migrate
```

### 6. Create Superuser (Admin)
```bash
python manage.py createsuperuser
# Enter username, email, password
```

### 7. Load Sample Data (Optional)
```bash
python manage.py loaddata sample_cars  # If fixtures available
```

### 8. Run Development Server
```bash
python manage.py runserver
```

Visit: http://localhost:8000

## API Endpoints

### Cars API
- `GET /api/cars/` - List all available cars (paginated)
- `GET /api/cars/{id}/` - Get car details
- `GET /api/cars/{id}/availability/` - Get availability for next 30 days

### Bookings API
- `GET /api/bookings/` - List user's bookings
- `POST /api/bookings/` - Create new booking
- `PATCH /api/bookings/{id}/` - Update booking
- `DELETE /api/bookings/{id}/` - Delete booking
- `POST /api/bookings/{id}/cancel/` - Cancel booking
- `POST /api/bookings/{id}/confirm/` - Confirm booking (admin)

### API Authentication
- Use session authentication for web
- Token authentication can be enabled for mobile apps

## Odoo Integration

### Setup Odoo Connection

1. **Update Settings** (location_voiture/settings.py):
```python
ODOO_CONFIG = {
    'BASE_URL': 'http://your-odoo-server:8069',
    'DATABASE': 'your_odoo_db',
    'USERNAME': 'admin',
    'PASSWORD': 'your_password',
    'USE_XMLRPC': True,  # Set to False for REST API
}
```

2. **Test Connection**:
```python
from odoo_integration import OdooConnector
connector = OdooConnector()
print(connector.test_connection())
```

3. **Sync Cars from Odoo**:
```python
from odoo_integration import SyncManager, OdooConnector

connector = OdooConnector()
sync = SyncManager(connector)
result = sync.sync_cars_from_odoo()
print(result)
```

4. **Sync Booking to Odoo**:
```python
from cars.models import Booking
from odoo_integration import SyncManager, OdooConnector

booking = Booking.objects.last()
sync = SyncManager(OdooConnector())
odoo_id = sync.sync_booking_to_odoo(booking)
```

## Usage Examples

### For Developers

#### Fetch Cars from Odoo
```python
from odoo_integration.odoo_connector import OdooConnector

connector = OdooConnector()
cars = connector.fetch_cars()
for car in cars:
    print(f"{car['name']} - ${car['daily_rate']}")
```

#### Create Booking Programmatically
```python
from cars.models import Car, Customer, Booking
from decimal import Decimal

customer = Customer.objects.get(user__username='john')
car = Car.objects.get(id=1)

booking = Booking.objects.create(
    customer=customer,
    car=car,
    start_date='2025-01-15 10:00',
    end_date='2025-01-20 10:00',
    pickup_location='Downtown Office',
    return_location='Downtown Office',
    daily_rate=car.daily_rate,
    number_of_days=5,
)
booking.calculate_cost()
booking.save()
```

### For End Users

1. **Sign Up**: Go to `/accounts/signup/` and create an account
2. **Complete Profile**: Fill in your address and license information
3. **Browse Cars**: Visit `/cars/` to see available vehicles
4. **Make a Booking**: Click on a car and fill in the booking form
5. **Confirm Booking**: Review details and confirm your reservation
6. **View Bookings**: Access your dashboard at `/cars/dashboard/`

## Admin Panel

Access the admin panel at: `http://localhost:8000/admin/`

### Manage:
- Cars (add, edit, delete, update status)
- Bookings (view, confirm, cancel)
- Customers (view profiles, verify customers)
- Availability calendar

## Customization

### Add Custom Fields
Edit `cars/models.py` to add fields to Car, Booking, or Customer models.

### Customize Templates
Modify HTML templates in `cars/templates/cars/` and `accounts/templates/accounts/`

### Add More Features
- Payment integration (Stripe, PayPal)
- Email notifications
- SMS notifications
- Advanced reporting
- Mobile app (React Native, Flutter)

## Database Models

### Car
- registration_number, make, model, year
- fuel_type, transmission, seats, mileage
- daily_rate, status (AVAILABLE, RENTED, MAINTENANCE, RESERVED)
- image, description, features
- odoo_id (link to Odoo)

### Booking
- booking_reference, customer, car
- start_date, end_date
- pickup_location, return_location
- daily_rate, number_of_days, total_cost
- status (PENDING, CONFIRMED, ACTIVE, COMPLETED, CANCELLED)
- payment_status (UNPAID, PAID, PARTIAL, REFUNDED)
- odoo_id

### Customer
- user (linked to Django User)
- phone_number, address, city, postal_code, country
- license_number, license_expiry
- total_rentals, total_spent
- is_verified, odoo_id

### Availability
- car, date, is_available
- Tracks which dates are available for each car

## Troubleshooting

### Issue: "Odoo authentication failed"
- Check Odoo server is running
- Verify credentials in settings.py
- Ensure database name is correct

### Issue: "No cars displayed"
- Run `python manage.py migrate`
- Add cars via admin panel or sync from Odoo
- Check car status is set to 'AVAILABLE'

### Issue: Migrations failing
- Delete `db.sqlite3` and migrations folders
- Run `python manage.py makemigrations`
- Run `python manage.py migrate`

## Deployment

### For Production
1. Set `DEBUG=False` in settings.py
2. Change `SECRET_KEY` to a secure random value
3. Use PostgreSQL instead of SQLite
4. Use environment variables for all secrets
5. Set up proper logging
6. Use Gunicorn/uWSGI with Nginx
7. Enable HTTPS/SSL

## Contributing
Contributions are welcome! Please follow Django best practices and include tests for new features.

## License
MIT License - feel free to use this project for personal and commercial projects.

## Support
For issues, questions, or suggestions, please create an issue in the repository.

---

**Last Updated**: December 2025
**Django Version**: 4.2.7
**Python Version**: 3.8+
