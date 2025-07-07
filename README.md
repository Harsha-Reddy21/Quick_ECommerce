# Quick Commerce Medicine Delivery API

A FastAPI-based backend for a quick commerce medicine delivery platform with user authentication, medicine catalog management, prescription handling, and rapid delivery functionality.

## Features

- User authentication and medical profiles
- Medicine catalog with search, filtering, and categorization
- Prescription upload, verification, and management
- Shopping cart with prescription validation
- Order processing and real-time tracking
- Quick delivery (10-30 minute promise)
- Location-based services for nearby pharmacies

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd Quick_ECommerce
```

2. Create a virtual environment and activate it:

```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up PostgreSQL database:

```bash
# Install PostgreSQL if not already installed
# Create a database named 'quickcommerce'
createdb quickcommerce  # If you have PostgreSQL CLI tools installed

# Or using SQL:
# psql -U postgres
# CREATE DATABASE quickcommerce;
# \q

# Update .env file with your database credentials
```

5. Check database connection:

```bash
python check_db_connection.py
```

6. Initialize the database:

```bash
python create_tables.py
```

## Running the Application

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

The API will be available at http://localhost:8000

API documentation will be available at:
- http://localhost:8000/docs (Swagger UI)
- http://localhost:8000/redoc (ReDoc)

## API Endpoints

### Authentication & Users:
- POST /auth/register - Register new user with medical profile
- POST /auth/login - User login
- GET /auth/me - Get current user profile
- PUT /auth/profile - Update user profile
- POST /auth/verify-phone - Verify phone number for delivery

### Medicines:
- GET /medicines - Get all medicines
- POST /medicines - Add new medicine (pharmacy admin only)
- PUT /medicines/{id} - Update medicine details (pharmacy admin only)
- DELETE /medicines/{id} - Remove medicine (pharmacy admin only)
- GET /medicines/search - Search medicines with filters
- GET /medicines/{id}/alternatives - Get alternative medicines
- PATCH /medicines/{id}/stock - Update medicine stock levels

### Medicine Categories:
- GET /categories - Get all medicine categories
- POST /categories - Create new category (pharmacy admin)
- PUT /categories/{id} - Update category (pharmacy admin)
- DELETE /categories/{id} - Delete category (pharmacy admin)

### Prescriptions:
- POST /prescriptions/upload - Upload prescription image
- GET /prescriptions - Get user's prescriptions
- GET /prescriptions/{id} - Get specific prescription details
- PUT /prescriptions/{id}/verify - Verify prescription (pharmacist only)
- GET /prescriptions/{id}/medicines - Get medicines from prescription

### Shopping Cart:
- GET /cart - Get user's cart
- POST /cart/items - Add medicine to cart
- PUT /cart/items/{id} - Update cart item quantity
- DELETE /cart/items/{id} - Remove medicine from cart
- DELETE /cart - Clear entire cart
- POST /cart/validate-prescriptions - Validate prescription medicines in cart

### Orders & Delivery:
- POST /orders - Create order from cart
- GET /orders - Get user's orders
- GET /orders/{id} - Get specific order details
- PATCH /orders/{id}/status - Update order status
- GET /orders/{id}/track - Real-time order tracking
- POST /orders/{id}/delivery-proof - Upload delivery confirmation

### Quick Delivery Features:
- GET /delivery/estimate - Get delivery time estimate
- GET /delivery/partners - Get available delivery partners
- POST /delivery/emergency - Create emergency medicine delivery request
- GET /nearby-pharmacies - Find nearby pharmacies with stock

## Default Users

- Admin User:
  - Email: admin@quickcommerce.com
  - Password: admin123

- Delivery Partner:
  - Email: delivery@quickcommerce.com
  - Password: delivery123