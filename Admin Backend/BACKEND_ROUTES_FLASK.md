# Flask Backend Routes Structure

This document outlines the Flask backend routes needed for the Admin Frontend.

## Project Structure

```
backend/
├── app.py                 # Main Flask app
├── config.py              # Configuration
├── requirements.txt       # Dependencies
├── models/
│   ├── __init__.py
│   ├── user.py           # Admin user model
│   ├── product.py        # Product model
│   ├── order.py          # Order model
│   ├── customer.py       # Customer model
│   ├── faq.py           # FAQ model
│   ├── promo.py         # Promo code model
│   └── settings.py      # Settings model
├── routes/
│   ├── __init__.py
│   ├── auth.py          # Authentication routes
│   ├── dashboard.py     # Dashboard routes
│   ├── products.py      # Products routes
│   ├── orders.py        # Orders routes
│   ├── customers.py     # Customers routes
│   ├── inventory.py     # Inventory routes
│   ├── faq.py          # FAQ routes
│   ├── promo.py        # Promo routes
│   ├── analysis.py     # Analytics routes
│   ├── settings.py     # Settings routes
│   └── search.py       # Search routes
├── utils/
│   ├── __init__.py
│   ├── auth.py         # JWT/auth helpers
│   ├── validators.py   # Input validation
│   └── helpers.py      # Utility functions
└── uploads/            # Uploaded files directory
```

## Required Flask Packages

```txt
Flask==3.0.0
Flask-CORS==4.0.0
Flask-JWT-Extended==4.6.0
Flask-SQLAlchemy==3.1.1
Flask-Migrate==4.0.5
SQLAlchemy==2.0.23
PyMySQL==1.1.0  # or psycopg2 for PostgreSQL
python-dotenv==1.0.0
werkzeug==3.0.1  # For secure filenames
```

## Route Definitions

### 1. Authentication Routes (`routes/auth.py`)

```python
POST   /api/auth/login              # Login admin user
POST   /api/auth/logout             # Logout (optional)
GET    /api/auth/verify             # Verify JWT token
POST   /api/auth/refresh            # Refresh JWT token
```

### 2. Dashboard Routes (`routes/dashboard.py`)

```python
GET    /api/dashboard/stats         # Get dashboard statistics
GET    /api/dashboard/recent-orders # Get recent orders
GET    /api/dashboard/top-products  # Get top selling products
```

### 3. Products Routes (`routes/products.py`)

```python
GET    /api/products                # List products (with filters)
GET    /api/products/:id            # Get product by ID
POST   /api/products               # Create new product
PUT    /api/products/:id            # Update product
DELETE /api/products/:id           # Delete product
POST   /api/products/:id/image     # Upload product image
GET    /api/products/categories     # Get all categories
GET    /api/products/pet-types      # Get all pet types
```

**Query Parameters for GET /api/products:**
- `search`: Search in name, SKU, description
- `category`: Filter by category
- `pet_type`: Filter by pet type
- `stock_status`: in-stock, low-stock, out-of-stock
- `page`: Page number (pagination)
- `per_page`: Items per page

### 4. Orders Routes (`routes/orders.py`)

```python
GET    /api/orders                  # List orders (with status filter)
GET    /api/orders/:id               # Get order details
PUT    /api/orders/:id               # Update order
DELETE /api/orders/:id               # Delete order
GET    /api/orders/:id/items         # Get order items
GET    /api/orders/export/csv         # Export orders to CSV
```

**Query Parameters for GET /api/orders:**
- `status`: processing, shipped, completed, cancelled
- `customer`: Filter by customer name/ID
- `date_from`: Start date
- `date_to`: End date
- `page`: Page number
- `per_page`: Items per page

### 5. Customers Routes (`routes/customers.py`)

```python
GET    /api/customers                # List customers (with filters)
GET    /api/customers/:id            # Get customer details
PUT    /api/customers/:id/block      # Block/unblock customer
DELETE /api/customers/:id            # Delete customer
GET    /api/customers/stats          # Customer statistics
GET    /api/customers/export/csv      # Export customers to CSV
GET    /api/customers/:id/orders     # Get customer's orders
```

**Query Parameters for GET /api/customers:**
- `search`: Search in name, email, location
- `status`: active, blocked
- `location`: Filter by location
- `page`: Page number
- `per_page`: Items per page

### 6. Inventory Routes (`routes/inventory.py`)

```python
GET    /api/inventory                # List inventory
GET    /api/inventory/stats          # Inventory statistics
PUT    /api/inventory/:id/stock      # Update single product stock
PUT    /api/inventory/bulk-update    # Bulk update stock
POST   /api/inventory/notify-users    # Notify users about stock
```

**Query Parameters for GET /api/inventory:**
- `search`: Search products
- `category`: Filter by category
- `pet_type`: Filter by pet type
- `stock_status`: in-stock, low-stock, out-of-stock

### 7. FAQ Routes (`routes/faq.py`)

```python
GET    /api/faq                      # List FAQs
GET    /api/faq/:id                  # Get FAQ by ID
POST   /api/faq                      # Create FAQ
PUT    /api/faq/:id                  # Update FAQ
DELETE /api/faq/:id                  # Delete FAQ
GET    /api/faq/categories           # Get FAQ categories
PUT    /api/faq/:id/feedback         # Update FAQ feedback
```

**Query Parameters for GET /api/faq:**
- `search`: Search in question/answer
- `category`: Filter by category
- `page`: Page number
- `per_page`: Items per page

### 8. Promo Codes Routes (`routes/promo.py`)

```python
GET    /api/promo                    # List promo codes
GET    /api/promo/:id                # Get promo by ID
POST   /api/promo                    # Create promo code
PUT    /api/promo/:id                # Update promo code
DELETE /api/promo/:id                # Delete promo code
GET    /api/promo/validate/:code     # Validate promo code
```

### 9. Analysis Routes (`routes/analysis.py`)

```python
GET    /api/analysis/sales            # Sales data for charts
GET    /api/analysis/orders           # Orders count data
GET    /api/analysis/product-sales    # Product-wise sales
GET    /api/analysis/monthly-growth   # Monthly growth data
GET    /api/analysis/time-range       # Custom time range analytics
```

**Query Parameters for analysis routes:**
- `start_date`: Start date (YYYY-MM-DD)
- `end_date`: End date (YYYY-MM-DD)
- `year`: Filter by year

### 10. Settings Routes (`routes/settings.py`)

```python
GET    /api/settings                 # Get all settings
PUT    /api/settings                 # Update settings
GET    /api/settings/payment-modes    # Get payment modes
PUT    /api/settings/payment-modes    # Update payment modes
GET    /api/settings/delivery-charges # Get delivery charges
PUT    /api/settings/delivery-charges # Update delivery charges
GET    /api/settings/exempted-areas  # Get exempted pincodes
PUT    /api/settings/exempted-areas  # Update exempted pincodes
```

### 11. Search Routes (`routes/search.py`)

```python
GET    /api/search                   # Global search
```

**Query Parameters:**
- `query`: Search term (required)
- `type`: all, products, customers, orders (default: all)
- `limit`: Number of results per type (default: 10)

### 12. Utility Routes

```python
POST   /api/upload/image             # Upload image file
GET    /api/health                   # Health check
```

## Example Flask App Structure

### `app.py`

```python
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from routes import auth, dashboard, products, orders, customers, inventory, faq, promo, analysis, settings, search

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
CORS(app)
jwt = JWTManager(app)

# Register blueprints
app.register_blueprint(auth.bp, url_prefix='/api/auth')
app.register_blueprint(dashboard.bp, url_prefix='/api/dashboard')
app.register_blueprint(products.bp, url_prefix='/api/products')
app.register_blueprint(orders.bp, url_prefix='/api/orders')
app.register_blueprint(customers.bp, url_prefix='/api/customers')
app.register_blueprint(inventory.bp, url_prefix='/api/inventory')
app.register_blueprint(faq.bp, url_prefix='/api/faq')
app.register_blueprint(promo.bp, url_prefix='/api/promo')
app.register_blueprint(analysis.bp, url_prefix='/api/analysis')
app.register_blueprint(settings.bp, url_prefix='/api/settings')
app.register_blueprint(search.bp, url_prefix='/api/search')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

### Example Route File Structure (`routes/products.py`)

```python
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Product
from utils.validators import validate_product_data

bp = Blueprint('products', __name__)

@bp.route('', methods=['GET'])
@jwt_required()
def get_products():
    """Get list of products with optional filters"""
    search = request.args.get('search', '')
    category = request.args.get('category', '')
    pet_type = request.args.get('pet_type', '')
    stock_status = request.args.get('stock_status', '')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Build query
    query = Product.query
    
    if search:
        query = query.filter(
            (Product.name.contains(search)) |
            (Product.sku.contains(search)) |
            (Product.description.contains(search))
        )
    
    if category:
        query = query.filter(Product.category == category)
    
    if pet_type:
        query = query.filter(Product.pet_type == pet_type)
    
    if stock_status:
        if stock_status == 'in-stock':
            query = query.filter(Product.stock > 10)
        elif stock_status == 'low-stock':
            query = query.filter(Product.stock > 0, Product.stock <= 10)
        elif stock_status == 'out-of-stock':
            query = query.filter(Product.stock == 0)
    
    # Pagination
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    products = pagination.items
    
    return jsonify({
        'products': [p.to_dict() for p in products],
        'total': pagination.total,
        'page': page,
        'per_page': per_page,
        'pages': pagination.pages
    })

@bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_product(id):
    """Get single product by ID"""
    product = Product.query.get_or_404(id)
    return jsonify(product.to_dict())

@bp.route('', methods=['POST'])
@jwt_required()
def create_product():
    """Create new product"""
    data = request.get_json()
    
    # Validate data
    errors = validate_product_data(data)
    if errors:
        return jsonify({'errors': errors}), 400
    
    # Create product
    product = Product(**data)
    db.session.add(product)
    db.session.commit()
    
    return jsonify(product.to_dict()), 201

@bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_product(id):
    """Update product"""
    product = Product.query.get_or_404(id)
    data = request.get_json()
    
    # Update fields
    for key, value in data.items():
        if hasattr(product, key):
            setattr(product, key, value)
    
    db.session.commit()
    return jsonify(product.to_dict())

@bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_product(id):
    """Delete product"""
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted'}), 200

@bp.route('/categories', methods=['GET'])
@jwt_required()
def get_categories():
    """Get all product categories"""
    categories = db.session.query(Product.category).distinct().all()
    return jsonify([cat[0] for cat in categories])

@bp.route('/pet-types', methods=['GET'])
@jwt_required()
def get_pet_types():
    """Get all pet types"""
    pet_types = db.session.query(Product.pet_type).distinct().all()
    return jsonify([pt[0] for pt in pet_types])
```

## Authentication Middleware

Use Flask-JWT-Extended for JWT-based authentication:

```python
# In utils/auth.py
from flask_jwt_extended import create_access_token, verify_jwt_in_request

def login_user(user):
    access_token = create_access_token(identity=user.id)
    return access_token

# Protect routes with @jwt_required() decorator
```

## Response Format

Standard JSON response format:

```python
# Success
{
    "data": {...},
    "message": "Success message"
}

# Error
{
    "error": "Error message",
    "errors": {...}  # For validation errors
}

# List with pagination
{
    "data": [...],
    "total": 100,
    "page": 1,
    "per_page": 10,
    "pages": 10
}
```

## Database Models Needed

1. **User** - Admin users
2. **Product** - Products with categories, pet types, stock
3. **Order** - Orders with status, customer reference
4. **OrderItem** - Individual items in orders
5. **Customer** - Customer information
6. **FAQ** - FAQ questions and answers
7. **PromoCode** - Promotional codes
8. **Settings** - Application settings (payment modes, delivery charges, etc.)

## Notes

- Use Flask-CORS to enable CORS for your Vue frontend
- Implement proper error handling for all routes
- Use SQLAlchemy for database ORM
- Implement pagination for list endpoints
- Validate all input data
- Use JWT tokens for authentication
- Store uploaded images in `uploads/` directory
- Use environment variables for sensitive configuration

