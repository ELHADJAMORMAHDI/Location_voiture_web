// Main application JavaScript
// Location Voiture - Car Rental System

document.addEventListener('DOMContentLoaded', function () {
    console.log('Application loaded');

    // Initialize tooltips
    initializeTooltips();

    // Initialize date pickers
    initializeDatePickers();

    // Setup form validation
    setupFormValidation();
});

// Initialize Bootstrap tooltips
function initializeTooltips() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Initialize date pickers for booking form
function initializeDatePickers() {
    var startDateInput = document.getElementById('id_start_date');
    var endDateInput = document.getElementById('id_end_date');

    if (startDateInput && endDateInput) {
        startDateInput.type = 'date';
        endDateInput.type = 'date';

        // Set minimum date to today
        var today = new Date().toISOString().split('T')[0];
        startDateInput.min = today;

        // Update end date minimum when start date changes
        startDateInput.addEventListener('change', function () {
            endDateInput.min = this.value;
        });
    }
}

// Form validation
function setupFormValidation() {
    var forms = document.querySelectorAll('.needs-validation');

    Array.prototype.slice.call(forms).forEach(function (form) {
        form.addEventListener('submit', function (event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
}

// Format currency for display
function formatCurrency(value) {
    return new Intl.NumberFormat('fr-FR', {
        style: 'currency',
        currency: 'EUR'
    }).format(value);
}

// Calculate booking cost
function calculateBookingCost(dailyRate, numberOfDays) {
    if (dailyRate && numberOfDays) {
        var subtotal = dailyRate * numberOfDays;
        var insurance = subtotal * 0.10; // 10% insurance
        var total = subtotal + insurance;
        return {
            subtotal: subtotal,
            insurance: insurance,
            total: total
        };
    }
    return null;
}

// Cancel booking with confirmation
function cancelBooking(bookingId) {
    if (confirm('Are you sure you want to cancel this booking?')) {
        fetch('/api/bookings/' + bookingId + '/cancel/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCsrfToken(),
                'Content-Type': 'application/json'
            }
        })
            .then(response => {
                if (response.ok) {
                    alert('Booking cancelled successfully');
                    location.reload();
                } else {
                    alert('Error cancelling booking');
                }
            })
            .catch(error => console.error('Error:', error));
    }
}

// Get CSRF token from cookie
function getCsrfToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]')?.value ||
        document.cookie.split('; ').find(row => row.startsWith('csrftoken='))?.split('=')[1];
}

// Show loading spinner
function showLoading(element) {
    element.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Loading...';
    element.disabled = true;
}

// Hide loading spinner
function hideLoading(element, text) {
    element.innerHTML = text;
    element.disabled = false;
}

// Format date for display
function formatDate(dateString) {
    var options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('fr-FR', options);
}
