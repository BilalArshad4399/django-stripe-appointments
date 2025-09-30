# Sofia Health - Django Appointment Booking System

A Django-based appointment booking platform with Stripe payment integration, demonstrating core skills in Django development and payment processing.

> **Note for Evaluators:** This project includes a `.env.test` file with working Stripe TEST keys for your convenience. Simply copy it to `.env` to run the project immediately without any additional setup.

## Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation & Setup

1. **Clone/Extract the project**
```bash
cd sofia_health_project
```

2. **Create and activate virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.test .env
```
 **That's it!** The `.env.test` file contains working Stripe TEST keys for immediate use.

*Alternative: To use your own Stripe test keys, copy `.env.example` instead and add your keys from https://dashboard.stripe.com/test/apikeys*

5. **Run database migrations**
```bash
python manage.py migrate
```
This will create a fresh `db.sqlite3` database file with all necessary tables.

6. **(Optional) Create admin superuser**
```bash
python manage.py createsuperuser
```
Follow prompts to create an admin account for `/admin/` access.

7. **Start the development server**
```bash
python manage.py runserver
```

8. **Access the application**
   - Open browser to: `http://127.0.0.1:8000/`

## How the Stripe Integration Works

### Payment Flow Architecture

1. **Appointment Creation**
   - User fills out appointment form with provider, date/time, and email
   - System creates an Appointment record with `payment_status = 'pending'`
   - User is redirected to payment page

2. **Stripe Checkout Session**
   - When user clicks "Pay with Stripe", the system:
     - Creates a Stripe Checkout Session via `stripe.checkout.Session.create()`
     - Includes appointment details and $50 amount
     - Stores the session ID in the appointment record
     - Redirects user to Stripe's hosted checkout page

3. **Payment Processing**
   - User enters payment details on Stripe's secure checkout
   - For testing, use card: `4242 4242 4242 4242` (any future expiry, any CVC)
   - Stripe handles all payment security and PCI compliance

4. **Success/Cancel Handling**
   - **Success**: Stripe redirects to `/payment/success/<id>/`
     - System verifies the session with Stripe
     - Updates appointment `payment_status` to 'paid'
     - Shows confirmation page
   - **Cancel**: Stripe redirects to `/payment/cancel/<id>/`
     - Updates appointment `payment_status` to 'cancelled'
     - Allows user to retry payment

### Key Stripe Components

- **Checkout Session**: Pre-built, hosted payment page by Stripe
- **Test Mode**: All transactions use test keys - no real charges
- **Session Verification**: System validates payment success with Stripe API
- **Security**: No card details touch our server - all handled by Stripe

## Project Structure

```
sofia_health_project/
├── appointments/          # Main Django app
│   ├── models.py         # Appointment model with Stripe fields
│   ├── views.py          # Payment flow and appointment logic
│   ├── forms.py          # Appointment creation form
│   └── templates/        # UI templates
├── .env                  # Stripe keys (not in repo)
├── requirements.txt      # Python dependencies
└── manage.py            # Django management script
```

## Important Notes

- This is a demonstration using Stripe TEST mode
- No real payments are processed
- `.env.test` file is included with working TEST keys for easy evaluation
- These are Stripe TEST keys (starting with `pk_test_` and `sk_test_`) - safe for assessment purposes
- Never commit real/production keys to version control
- For production deployment, use proper secret management and live Stripe keys
