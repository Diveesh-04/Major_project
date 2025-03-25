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

