# Quick Start Guide - Location Voiture Django Project

## What You Have

A complete, production-ready Django car rental web application with:
- ✅ Full car rental management system
- ✅ Customer authentication and profiles
- ✅ Advanced booking system with cost calculations
- ✅ REST API with Django REST Framework
- ✅ Odoo ERP integration (XML-RPC & REST API)
- ✅ Responsive Bootstrap 5 templates
- ✅ Admin panel with custom actions
- ✅ Complete documentation

## Project Structure Summary

```
location_voiture/
├── Django Project Files (settings, urls, wsgi, asgi)
├── cars/                    - Main app (cars, bookings, availability)
├── accounts/               - Authentication (login, signup, profiles)
├── odoo_integration/       - Odoo synchronization module
├── templates/              - Base templates (home page)
├── requirements.txt        - All dependencies
├── README.md              - Full documentation
└── Setup Scripts          - setup.bat (Windows), setup.sh (Linux/Mac)
```

## Getting Started (Windows)

### Step 1: Open PowerShell in the project directory
```powershell
cd "d:\projet erp\Location_voiture_web\location_voiture"
```

### Step 2: Run setup script
```powershell
# One of these will work depending on PowerShell execution policy
.\setup.bat

# Or if that doesn't work:
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
```

### Step 3: Start the server
```powershell
python manage.py runserver
```

### Step 4: Access the application
- **Home Page**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin
- **API Docs**: http://localhost:8000/api/cars/

## Key URLs

### User-Facing
- `/` - Home page
- `/cars/` - Browse cars
- `/cars/<id>/` - Car details
- `/cars/booking/create/` - Make a booking
- `/cars/dashboard/` - Customer dashboard
- `/accounts/signup/` - Register
- `/accounts/login/` - Login

### API
- `/api/cars/` - List cars
- `/api/cars/<id>/` - Car details
- `/api/bookings/` - User bookings
- `/api/bookings/` (POST) - Create booking

### Admin
- `/admin/` - Django admin panel

## Database Models

### Car
Stores vehicle information with status tracking and Odoo links

### Booking
Manages reservations with automatic cost calculation

### Customer
Extended user profile with license info and rental history

### Availability
Tracks which dates cars are available

## Odoo Integration

Located in `odoo_integration/` folder:

### odoo_connector.py
- XML-RPC connection to Odoo
- REST API fallback
- Fetch cars from fleet.vehicle
- Create bookings in Odoo
- Sync customers

### sync_manager.py
- Bidirectional sync between Django and Odoo
- Maintains odoo_id references
- Status reporting

### Usage Example
```python
from odoo_integration import OdooConnector, SyncManager

# Test connection
connector = OdooConnector()
connector.test_connection()

# Fetch cars from Odoo
cars = connector.fetch_cars()

# Sync cars to Django
sync = SyncManager(connector)
result = sync.sync_cars_from_odoo()
```

## Common Tasks

### Add a Car to the System
```python
python manage.py shell
from cars.models import Car
Car.objects.create(
    registration_number='ABC123',
    make='Toyota',
    model='Camry',
    year=2023,
    daily_rate=50,
    fuel_type='GASOLINE',
    transmission='AUTOMATIC',
    seats=5,
    color='Silver'
)
```

### Sync Cars from Odoo
```bash
python manage.py sync_cars_from_odoo
```

### Create Admin User
```bash
python manage.py createsuperuser
```

## Important Files to Know

- `location_voiture/settings.py` - Configuration (DATABASES, INSTALLED_APPS, etc)
- `location_voiture/urls.py` - Main URL routing
- `cars/models.py` - Car, Booking, Customer, Availability models
- `cars/views.py` - Web views
- `cars/views_api.py` - REST API views
- `odoo_integration/odoo_connector.py` - Odoo connection

## Environment Variables

Create `.env` file with:
```env
DEBUG=True
SECRET_KEY=your-secret-key-change-in-production
ODOO_BASE_URL=http://localhost:8069
ODOO_DATABASE=odoo_db
ODOO_USERNAME=admin
ODOO_PASSWORD=admin
```

## Testing the API

### Using cURL
```bash
# List cars
curl http://localhost:8000/api/cars/

# Get car details
curl http://localhost:8000/api/cars/1/

# Create booking (requires authentication)
curl -X POST http://localhost:8000/api/bookings/ \
  -H "Content-Type: application/json" \
  -d '{"car":1,"start_date":"2025-01-15T10:00","end_date":"2025-01-20T10:00",...}'
```

### Using Python Requests
```python
import requests

# Get cars
response = requests.get('http://localhost:8000/api/cars/')
cars = response.json()

# Get car details
response = requests.get('http://localhost:8000/api/cars/1/')
car = response.json()
```

## Features Summary

### Implemented ✓
- [x] User authentication (login, signup, logout)
- [x] Customer profiles with license info
- [x] Car browsing with filters
- [x] Booking system with cost calculation
- [x] Admin panel with custom actions
- [x] REST API
- [x] Odoo integration (XML-RPC & REST)
- [x] Responsive design
- [x] Booking confirmation
- [x] Dashboard

### To Add (Optional)
- [ ] Payment gateway (Stripe, PayPal)
- [ ] Email notifications
- [ ] SMS notifications
- [ ] Advanced reporting
- [ ] Review system
- [ ] Mobile app
- [ ] Advanced analytics

## Customization Guide

### Add Custom Field to Car
1. Edit `cars/models.py`
2. Add field: `custom_field = models.CharField(max_length=100)`
3. Run: `python manage.py makemigrations`
4. Run: `python manage.py migrate`
5. Update admin: edit `cars/admin.py`
6. Update templates: edit `cars/templates/cars/car_detail.html`

### Customize Templates
All templates use Bootstrap 5 and can be modified:
- Base: `templates/base.html`
- Cars: `cars/templates/cars/`
- Accounts: `accounts/templates/accounts/`

### Configure Odoo Connection
Edit `location_voiture/settings.py`:
```python
ODOO_CONFIG = {
    'BASE_URL': 'http://your-odoo-server:8069',
    'DATABASE': 'your_database',
    'USERNAME': 'admin',
    'PASSWORD': 'password',
    'USE_XMLRPC': True,  # or False for REST API
}
```

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'django'"
**Solution**: Install dependencies:
```bash
pip install -r requirements.txt
```

### Issue: "DatabaseError" on first run
**Solution**: Run migrations:
```bash
python manage.py migrate
```

### Issue: Odoo connection fails
**Solution**: 
1. Verify Odoo server is running
2. Check credentials in settings.py
3. Test connection: `python manage.py shell`
   ```python
   from odoo_integration import OdooConnector
   connector = OdooConnector()
   connector.test_connection()
   ```

### Issue: Static files not loading
**Solution**: Collect static files:
```bash
python manage.py collectstatic --noinput
```

## Performance Tips

1. **Use database indexing** - Already done for main fields
2. **Enable caching** - Add Redis caching in settings.py
3. **Optimize queries** - Use select_related() and prefetch_related()
4. **Compress static files** - Use WhiteNoise or similar
5. **Use CDN** - For images and static files in production

## Security Notes

⚠️ **For Production**:
1. Change SECRET_KEY
2. Set DEBUG=False
3. Use environment variables for secrets
4. Set ALLOWED_HOSTS properly
5. Use HTTPS
6. Enable CSRF protection (already done)
7. Use strong database password
8. Set up proper logging

## Next Steps

1. **Add some test data** via admin panel
2. **Test bookings** by creating a booking
3. **Sync with Odoo** using the sync command
4. **Customize templates** with your branding
5. **Add payment processing** (Stripe integration)
6. **Deploy to production** (Heroku, AWS, DigitalOcean, etc.)

## Support Resources

- Django Docs: https://docs.djangoproject.com/
- Django REST Framework: https://www.django-rest-framework.org/
- Odoo Documentation: https://www.odoo.com/documentation/
- Bootstrap 5: https://getbootstrap.com/docs/5.0/

## Contact & Support

For issues, improvements, or questions:
1. Check the README.md in the project root
2. Review the code comments
3. Check the example files in odoo_integration/

---

**Happy Coding!** 🚗

You now have a complete, professional car rental system ready to customize and deploy.
