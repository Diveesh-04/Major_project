# ISAK Backend

This is the backend for the ISAK Fragrances e-commerce platform, built using Django and Django REST Framework. It provides APIs for managing users, products, categories, carts, and orders, along with authentication and payment integration.

---

## Features

- **User Authentication**: Custom user model with login, registration, and JWT-based authentication.
- **Product Management**: APIs for managing products and categories.
- **Cart Management**: Add, update, and remove items from the cart.
- **Order Management**: Checkout and payment integration using Razorpay.
- **Admin Panel**: Manage users, products, and orders via Django's admin interface.
- **Responsive Design**: Frontend integration with Bootstrap for a seamless user experience.

---

## Tech Stack

- **Backend Framework**: Django 5.1.6
- **API Framework**: Django REST Framework
- **Database**: SQLite (default, can be switched to PostgreSQL)
- **Authentication**: JWT (via `djangorestframework-simplejwt`)
- **Payment Gateway**: Razorpay
- **Frontend**: Bootstrap (integrated with Django templates)

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Diveesh-04/Major_project.git
   cd isak-backend
   
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Mac/Linux
   source venv/bin/activate  # On Mac/Linux
   
3. Install dependencies:
   ```bash
   pip install -r requirements.txt

4. Apply migrations:
   ```bash
   python manage.py migrate

5. Run the development server:
   ```bash
   python manage.py runserver

---

## API Endpoints

Authentication:
	•	POST /api/register/ - Register a new user
	•	POST /api/login/ - Obtain JWT tokens
	•	POST /api/token/refresh/ - Refresh JWT tokens
Products:
	•	GET /api/products/ - List all products
	•	GET /api/products/<id>/ - Retrieve product details
Categories:
	•	GET /api/categories/ - List all categories
Cart:
	•	GET /api/cart/ - View cart items
	•	POST /api/cart/ - Add item to cart
	•	PATCH /api/cart/<id>/ - Update cart item quantity
	•	DELETE /api/cart/<id>/ - Remove item from cart
Orders:
	•	POST /api/checkout/ - Create an order
	•	POST /api/payment/ - Razorpay payment integration

---

## Project Structure

﻿isak_backend/               # Root project directory
├── manage.py               # Django project management script
├── requirements.txt        # Project dependencies
├── db.sqlite3              # SQLite database (if used)
├── static/                 # Global static files (optional)
│   ├── css/
│   │   └── styles.css      # Global styles
│   ├── images/             # Global images
│   └── js/
│       └── scripts.js      # JavaScript files
├── store/                  # Main app for handling products, cart, and orders
│   ├── init.py
│   ├── admin.py            # Django admin configurations
│   ├── apps.py             # App configuration
│   ├── models.py           # Database models (Product, Category, Cart, Order, etc.)
│   ├── views.py            # API views and business logic
│   ├── urls.py             # URL routing for the store app
│   ├── serializers.py      # DRF serializers for API responses
│   ├── permissions.py      # Custom permissions (if any)
│   ├── tests.py            # Unit tests
│   ├── templates/          # HTML templates for frontend views
│   │   ├── base.html       # Base template
│   │   ├── home.html       # Home page template
│   │   ├── product_detail.html  # Product detail page
│   │   ├── cart.html       # Shopping cart page
│   │   ├── checkout.html   # Checkout page
│   │   ├── order_success.html  # Order completion page
│   │   ├── login.html      # Login page
│   │   └── register.html   # Sign-up page
│   ├── static/             # Static files specific to the store app
│   │   ├── css/
│   │   │   └── store_styles.css
│   │   ├── images/
│   │   └── js/
│   ├── forms.py            # Django forms (if using forms)
│   ├── signals.py          # Django signals (if any)
│   └── migrations/         # Database migrations
│       ├── init.py
│       ├── 0001_initial.py
│       ├── 0002_some_change.py
│       └── …
├── api/                    # API app for handling authentication, cart, etc.
│   ├── init.py
│   ├── views.py
│   ├── urls.py
│   ├── serializers.py
│   ├── permissions.py
│   ├── authentication.py
│   ├── models.py
│   ├── tests.py
│   ├── signals.py
│   ├── utils.py            # Helper functions (if any)
│   ├── forms.py
│   └── migrations/
├── users/                  # Custom user authentication app (if separate)
│   ├── init.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── serializers.py
│   ├── forms.py
│   ├── permissions.py
│   ├── authentication.py
│   ├── admin.py
│   ├── signals.py
│   ├── tests.py
│   ├── utils.py
│   └── migrations/
├── isak_backend/            # Main Django project settings
│   ├── init.py
│   ├── asgi.py
│   ├── wsgi.py
│   ├── settings.py         # Main Django settings (including database, static files, etc.)
│   ├── urls.py             # Root URL configuration
│   └── middleware.py       # Custom middleware (if any)
└── logs/                    # Log files (if needed)
├── debug.log
└── error.log

---

## Deployment

1. Install Gunicorn:
   ```bash
   pip install gunicorn

2. Collect static files:
   ```bash
   python manage.py collectstatic

3. Deploy using a platform like Heroku, AWS, or DigitalOcean.

---

## License

-This project is licensed under the MIT License. See the LICENSE file for details.

---

## Contact

For any inquiries, please contact:

Email: isak@gmail.com
Phone: +91 7571836190

