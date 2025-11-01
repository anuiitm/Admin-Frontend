# Flask Backend - Quick Reference

## All Routes Summary

### 🔐 Authentication (`/api/auth`)
- `POST /api/auth/login` - Login
- `GET /api/auth/verify` - Verify token
- `POST /api/auth/refresh` - Refresh token

### 📊 Dashboard (`/api/dashboard`)
- `GET /api/dashboard/stats` - Statistics (revenue, orders, customers, inventory)
- `GET /api/dashboard/recent-orders` - Recent orders
- `GET /api/dashboard/top-products` - Top selling products

### 📦 Products (`/api/products`)
- `GET /api/products` - List (filters: search, category, pet_type, stock_status)
- `GET /api/products/:id` - Get by ID
- `POST /api/products` - Create
- `PUT /api/products/:id` - Update
- `DELETE /api/products/:id` - Delete
- `POST /api/products/:id/image` - Upload image
- `GET /api/products/categories` - Get categories
- `GET /api/products/pet-types` - Get pet types

### 🛒 Orders (`/api/orders`)
- `GET /api/orders` - List (filter: status)
- `GET /api/orders/:id` - Get by ID
- `PUT /api/orders/:id` - Update
- `DELETE /api/orders/:id` - Delete
- `GET /api/orders/:id/items` - Get order items
- `GET /api/orders/export/csv` - Export CSV

### 👥 Customers (`/api/customers`)
- `GET /api/customers` - List (filters: search, status, location)
- `GET /api/customers/:id` - Get by ID
- `PUT /api/customers/:id/block` - Block/unblock
- `DELETE /api/customers/:id` - Delete
- `GET /api/customers/stats` - Statistics
- `GET /api/customers/export/csv` - Export CSV
- `GET /api/customers/:id/orders` - Customer orders

### 📊 Inventory (`/api/inventory`)
- `GET /api/inventory` - List (filters: search, category, pet_type, stock_status)
- `GET /api/inventory/stats` - Statistics
- `PUT /api/inventory/:id/stock` - Update stock
- `PUT /api/inventory/bulk-update` - Bulk update
- `POST /api/inventory/notify-users` - Notify users

### ❓ FAQ (`/api/faq`)
- `GET /api/faq` - List (filters: search, category)
- `GET /api/faq/:id` - Get by ID
- `POST /api/faq` - Create
- `PUT /api/faq/:id` - Update
- `DELETE /api/faq/:id` - Delete
- `GET /api/faq/categories` - Get categories
- `PUT /api/faq/:id/feedback` - Update feedback

### 🎫 Promo Codes (`/api/promo`)
- `GET /api/promo` - List
- `GET /api/promo/:id` - Get by ID
- `POST /api/promo` - Create
- `PUT /api/promo/:id` - Update
- `DELETE /api/promo/:id` - Delete
- `GET /api/promo/validate/:code` - Validate code

### 📈 Analysis (`/api/analysis`)
- `GET /api/analysis/sales` - Sales data
- `GET /api/analysis/orders` - Orders count
- `GET /api/analysis/product-sales` - Product-wise sales
- `GET /api/analysis/monthly-growth` - Monthly growth
- `GET /api/analysis/time-range` - Custom range

### ⚙️ Settings (`/api/settings`)
- `GET /api/settings` - Get all
- `PUT /api/settings` - Update all
- `GET /api/settings/payment-modes` - Get payment modes
- `PUT /api/settings/payment-modes` - Update payment modes
- `GET /api/settings/delivery-charges` - Get delivery charges
- `PUT /api/settings/delivery-charges` - Update charges
- `GET /api/settings/exempted-areas` - Get exempted pincodes
- `PUT /api/settings/exempted-areas` - Update exempted areas

### 🔍 Search (`/api/search`)
- `GET /api/search?query=...&type=all|products|customers|orders` - Global search

### 🛠️ Utility
- `POST /api/upload/image` - Upload image
- `GET /api/health` - Health check

## Flask Project Structure

```
backend/
├── app.py              # Main Flask app
├── config.py           # Configuration
├── requirements.txt    # Dependencies
├── models/             # SQLAlchemy models
├── routes/             # Blueprint routes
├── utils/              # Helpers & validators
└── uploads/            # File uploads
```

## Required Packages

```
Flask==3.0.0
Flask-CORS==4.0.0
Flask-JWT-Extended==4.6.0
Flask-SQLAlchemy==3.1.1
Flask-Migrate==4.0.5
SQLAlchemy==2.0.23
python-dotenv==1.0.0
```

## Total Routes: ~50 endpoints

All routes (except `/api/auth/login` and `/api/health`) should be protected with `@jwt_required()` decorator.

