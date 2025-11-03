# models.py
"""
models.py
Complete SQLAlchemy models for Pettry application.
"""

from datetime import datetime, date
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Index

# Initialize SQLAlchemy
db = SQLAlchemy()

# Rest of your models...


# -------------------------
# USER
# -------------------------
class User(db.Model):
    __tablename__ = "user"

    user_id = db.Column(db.Integer, primary_key=True)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    customer_code = db.Column(db.String(100), unique=True, index=True)
    full_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(50))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    country = db.Column(db.String(100))
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default='customer')
    date_joined = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    profile_image = db.Column(db.String(500))
    last_login = db.Column(db.DateTime)

    # Relationships
    products = db.relationship("Product", back_populates="uploader", lazy="dynamic")
    promo_codes = db.relationship("PromoCode", back_populates="creator", lazy="dynamic")
    dashboard_reports = db.relationship("DashboardReport", back_populates="generator", lazy="dynamic")
    faqs = db.relationship("FAQ", back_populates="created_by_user", lazy="dynamic")
    notifications = db.relationship("Notification", back_populates="user", lazy="dynamic")
    orders = db.relationship("Order", back_populates="user", lazy="dynamic")
    cart_items = db.relationship("CartItem", back_populates="user", lazy="dynamic")
    wishlist_items = db.relationship("WishlistItem", back_populates="user", lazy="dynamic")
    reviews = db.relationship("Review", back_populates="user", lazy="dynamic")
    delivery_addresses = db.relationship("DeliveryAddress", back_populates="user", lazy="dynamic")
    pet_profiles = db.relationship("PetProfile", back_populates="user", lazy="dynamic")
    support_tickets = db.relationship("SupportTicket", back_populates="user", foreign_keys="SupportTicket.user_id", lazy="dynamic")
    assigned_tickets = db.relationship("SupportTicket", back_populates="assigned_user", foreign_keys="SupportTicket.assigned_to", lazy="dynamic")
    payments = db.relationship("Payment", back_populates="user", lazy="dynamic")
    petpal_conversations = db.relationship("PetpalConversation", back_populates="user", lazy="dynamic")
    support_messages = db.relationship("SupportMessage", back_populates="sender", lazy="dynamic")
    inventory_updates = db.relationship("Inventory", back_populates="updated_by_user", lazy="dynamic")
    order_status_updates = db.relationship("OrderStatus", back_populates="updated_by_user", lazy="dynamic")
    activity_logs = db.relationship("AdminActivityLog", back_populates="user", lazy="dynamic")
    stock_movements = db.relationship("StockMovement", back_populates="user", lazy="dynamic")
    search_logs = db.relationship("SearchQueryLog", back_populates="user", lazy="dynamic")
    return_requests = db.relationship("ReturnRequest", back_populates="user", lazy="dynamic")

    def set_password(self, password):
        """Hash and set password"""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password against hash"""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.email}>'


# -------------------------
# PRODUCT
# -------------------------
class Product(db.Model):
    __tablename__ = "product"
    __table_args__ = (
        Index('idx_product_category_pet', 'category_name', 'pet_type'),
        Index('idx_product_active_featured', 'is_active', 'is_featured'),
    )

    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    sku = db.Column(db.String(255), unique=True, nullable=False, index=True)
    description = db.Column(db.Text)
    short_description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    discount_price = db.Column(db.Float)
    stock = db.Column(db.Integer, default=0, nullable=False)
    main_image_url = db.Column(db.String(500), nullable=False)
    weight = db.Column(db.Float)
    dimensions = db.Column(db.String(255))
    tags = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    category_name = db.Column(db.String(255), nullable=False)
    pet_type = db.Column(db.String(100), nullable=False)
    uploader_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_featured = db.Column(db.Boolean, default=False, nullable=False)
    avg_rating = db.Column(db.Float, default=0.0)
    review_count = db.Column(db.Integer, default=0)
    ingredients = db.Column(db.Text)
    features = db.Column(db.Text)
    status = db.Column(db.String(100), default='active')

    # Relationships
    uploader = db.relationship("User", back_populates="products")
    order_items = db.relationship("OrderItem", back_populates="product", lazy="dynamic")
    cart_items = db.relationship("CartItem", back_populates="product", lazy="dynamic")
    wishlist_items = db.relationship("WishlistItem", back_populates="product", lazy="dynamic")
    reviews = db.relationship("Review", back_populates="product", lazy="dynamic")
    product_analytics = db.relationship("ProductAnalytic", back_populates="product", lazy="dynamic")
    inventory_items = db.relationship("Inventory", back_populates="product", lazy="dynamic")
    stock_movements = db.relationship("StockMovement", back_populates="product", lazy="dynamic")
    category_id = db.Column(db.Integer, db.ForeignKey("category.category_id"))
    category = db.relationship("Category", back_populates="products")

    @property
    def current_price(self):
        """Return the effective price (discount if available, otherwise regular)"""
        return self.discount_price if self.discount_price else self.price

    @property
    def is_discounted(self):
        """Check if product has an active discount"""
        return self.discount_price is not None and self.discount_price < self.price

    def __repr__(self):
        return f'<Product {self.name}>'


# -------------------------
# PROMO_CODE
# -------------------------
class PromoCode(db.Model):
    __tablename__ = "promo_code"

    promo_id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(100), unique=True, nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    discount_type = db.Column(db.String(50), nullable=False)  # 'percentage' or 'fixed'
    discount_value = db.Column(db.Float, nullable=False)
    min_order_value = db.Column(db.Float, default=0)
    max_discount_amount = db.Column(db.Float)
    valid_from = db.Column(db.DateTime, nullable=False)
    valid_until = db.Column(db.DateTime, nullable=False)
    max_uses = db.Column(db.Integer)
    max_uses_per_user = db.Column(db.Integer, default=1)
    used_count = db.Column(db.Integer, default=0, nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey("user.user_id"))

    # Relationships
    creator = db.relationship("User", back_populates="promo_codes")
    orders = db.relationship("Order", back_populates="promo_code", lazy="dynamic")

    def is_valid(self, order_value=0):
        """Check if promo code is currently valid"""
        now = datetime.utcnow()
        return (
            self.active and
            self.valid_from <= now <= self.valid_until and
            order_value >= self.min_order_value and
            (self.max_uses is None or self.used_count < self.max_uses)
        )

    def calculate_discount(self, order_value):
        """Calculate discount amount for given order value"""
        if self.discount_type == 'percentage':
            discount = order_value * (self.discount_value / 100)
            if self.max_discount_amount:
                discount = min(discount, self.max_discount_amount)
            return discount
        elif self.discount_type == 'fixed':
            return min(self.discount_value, order_value)
        return 0

    def __repr__(self):
        return f'<PromoCode {self.code}>'


# -------------------------
# DASHBOARD_REPORT
# -------------------------
class DashboardReport(db.Model):
    __tablename__ = "dashboard_report"

    report_id = db.Column(db.Integer, primary_key=True)
    report_date = db.Column(db.Date, nullable=False, unique=True, index=True)
    total_sales = db.Column(db.Float, default=0)
    total_revenue = db.Column(db.Float, default=0)
    total_orders = db.Column(db.Integer, default=0)
    total_customers = db.Column(db.Integer, default=0)
    new_customers = db.Column(db.Integer, default=0)
    top_products = db.Column(db.Text)  # JSON string
    top_categories = db.Column(db.Text)  # JSON string
    avg_order_value = db.Column(db.Float, default=0)
    pending_orders = db.Column(db.Integer, default=0)
    low_stock_products = db.Column(db.Integer, default=0)
    generated_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    generator_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))

    # Relationships
    generator = db.relationship("User", back_populates="dashboard_reports")

    def __repr__(self):
        return f'<DashboardReport {self.report_date}>'


# -------------------------
# FAQ
# -------------------------
class FAQ(db.Model):
    __tablename__ = "faq"
    __table_args__ = (
        Index('idx_faq_category_active', 'category', 'is_active'),
    )

    faq_id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(1000), nullable=False)
    answer = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(255), nullable=False)
    display_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    view_count = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey("user.user_id"))

    # Relationships
    created_by_user = db.relationship("User", back_populates="faqs")

    def __repr__(self):
        return f'<FAQ {self.question[:50]}>'


# -------------------------
# NOTIFICATION
# -------------------------
class Notification(db.Model):
    __tablename__ = "notification"
    __table_args__ = (
        Index('idx_notification_user_read', 'user_id', 'is_read'),
    )

    notification_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    link = db.Column(db.String(500))
    is_read = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    read_at = db.Column(db.DateTime)

    # Relationships
    user = db.relationship("User", back_populates="notifications")

    def mark_as_read(self):
        """Mark notification as read"""
        self.is_read = True
        self.read_at = datetime.utcnow()

    def __repr__(self):
        return f'<Notification {self.title}>'


# -------------------------
# DELIVERY_ADDRESS
# -------------------------
class DeliveryAddress(db.Model):
    __tablename__ = "delivery_address"

    address_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    address_type = db.Column(db.String(100), nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    street_address = db.Column(db.String(500), nullable=False)
    landmark = db.Column(db.String(255))
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    pin_code = db.Column(db.String(30), nullable=False)
    is_default = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = db.relationship("User", back_populates="delivery_addresses")
    shipping_orders = db.relationship("Order", back_populates="shipping_address", foreign_keys="Order.shipping_address_id", lazy="dynamic")
    billing_orders = db.relationship("Order", back_populates="billing_address", foreign_keys="Order.billing_address_id", lazy="dynamic")

    @property
    def full_address(self):
        """Return formatted full address"""
        parts = [self.street_address]
        if self.landmark:
            parts.append(self.landmark)
        parts.extend([self.city, self.state, self.country, self.pin_code])
        return ", ".join(parts)

    def __repr__(self):
        return f'<DeliveryAddress {self.full_name} - {self.city}>'


# -------------------------
# ORDER
# -------------------------
class Order(db.Model):
    __tablename__ = "order"
    __table_args__ = (
        Index('idx_order_user_status', 'user_id', 'order_status'),
        Index('idx_order_date', 'order_date'),
    )

    order_id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(255), unique=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    discount_amount = db.Column(db.Float, default=0)
    shipping_cost = db.Column(db.Float, default=0)
    tax_amount = db.Column(db.Float, default=0)
    total_price = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(100), nullable=False)
    payment_status = db.Column(db.String(100), default='pending')
    order_status = db.Column(db.String(100), default='pending')
    shipping_address_id = db.Column(db.Integer, db.ForeignKey("delivery_address.address_id"))
    billing_address_id = db.Column(db.Integer, db.ForeignKey("delivery_address.address_id"))
    promo_code_id = db.Column(db.Integer, db.ForeignKey("promo_code.promo_id"))
    notes = db.Column(db.Text)
    delivered_at = db.Column(db.DateTime)
    cancelled_at = db.Column(db.DateTime)
    cancellation_reason = db.Column(db.String(500))

    # Relationships
    user = db.relationship("User", back_populates="orders")
    order_items = db.relationship("OrderItem", back_populates="order", lazy="dynamic", cascade="all, delete-orphan")
    payments = db.relationship("Payment", back_populates="order", lazy="dynamic", cascade="all, delete-orphan")
    order_statuses = db.relationship("OrderStatus", back_populates="order", lazy="dynamic", cascade="all, delete-orphan")
    promo_code = db.relationship("PromoCode", back_populates="orders")
    shipping_address = db.relationship("DeliveryAddress", foreign_keys=[shipping_address_id], back_populates="shipping_orders")
    billing_address = db.relationship("DeliveryAddress", foreign_keys=[billing_address_id], back_populates="billing_orders")
    shipments = db.relationship("Shipment", back_populates="order", lazy="dynamic", cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Order {self.order_number}>'


# -------------------------
# ORDER_ITEM
# -------------------------
class OrderItem(db.Model):
    __tablename__ = "order_item"

    order_item_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.order_id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.product_id"))
    product_name = db.Column(db.String(500), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price_at_purchase = db.Column(db.Float, nullable=False)
    discount_at_purchase = db.Column(db.Float, default=0)
    total_price = db.Column(db.Float, nullable=False)

    # Relationships
    order = db.relationship("Order", back_populates="order_items")
    product = db.relationship("Product", back_populates="order_items")
    return_requests = db.relationship("ReturnRequest", back_populates="order_item", lazy="dynamic", cascade="all, delete-orphan")

    def __repr__(self):
        return f'<OrderItem {self.product_name} x{self.quantity}>'


# -------------------------
# CART_ITEM
# -------------------------
class CartItem(db.Model):
    __tablename__ = "cart_item"
    __table_args__ = (
        db.UniqueConstraint('user_id', 'product_id', name='uq_cart_user_product'),
    )

    cart_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.product_id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    added_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = db.relationship("User", back_populates="cart_items")
    product = db.relationship("Product", back_populates="cart_items")

    @property
    def subtotal(self):
        """Calculate subtotal for this cart item"""
        return self.product.current_price * self.quantity if self.product else 0

    def __repr__(self):
        return f'<CartItem user:{self.user_id} product:{self.product_id}>'


# -------------------------
# WISHLIST_ITEM
# -------------------------
class WishlistItem(db.Model):
    __tablename__ = "wishlist_item"
    __table_args__ = (
        db.UniqueConstraint('user_id', 'product_id', name='uq_wishlist_user_product'),
    )

    wishlist_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.product_id"), nullable=False)
    added_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = db.relationship("User", back_populates="wishlist_items")
    product = db.relationship("Product", back_populates="wishlist_items")

    def __repr__(self):
        return f'<WishlistItem user:{self.user_id} product:{self.product_id}>'


# -------------------------
# REVIEW
# -------------------------
class Review(db.Model):
    __tablename__ = "review"
    __table_args__ = (
        db.UniqueConstraint('user_id', 'product_id', name='uq_review_user_product'),
        Index('idx_review_product_rating', 'product_id', 'rating'),
    )

    review_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.product_id"), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_verified_purchase = db.Column(db.Boolean, default=False, nullable=False)

    # Relationships
    user = db.relationship("User", back_populates="reviews")
    product = db.relationship("Product", back_populates="reviews")

    def __repr__(self):
        return f'<Review product:{self.product_id} rating:{self.rating}>'


# -------------------------
# PET_PROFILE
# -------------------------
class PetProfile(db.Model):
    __tablename__ = "pet_profile"

    pet_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    pet_type = db.Column(db.String(100), nullable=False)
    breed = db.Column(db.String(255))
    date_of_birth = db.Column(db.Date)
    weight = db.Column(db.Float)
    gender = db.Column(db.String(50))
    image_url = db.Column(db.String(500))
    medical_conditions = db.Column(db.Text)
    dietary_restrictions = db.Column(db.Text)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = db.relationship("User", back_populates="pet_profiles")
    petpal_conversations = db.relationship("PetpalConversation", back_populates="pet_profile", lazy="dynamic")

    @property
    def age(self):
        """Calculate pet's age in years"""
        if self.date_of_birth:
            today = date.today()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None

    def __repr__(self):
        return f'<PetProfile {self.name} ({self.pet_type})>'


# -------------------------
# SUPPORT_TICKET
# -------------------------
class SupportTicket(db.Model):
    __tablename__ = "support_ticket"
    __table_args__ = (
        Index('idx_ticket_status_priority', 'status', 'priority'),
    )

    ticket_id = db.Column(db.Integer, primary_key=True)
    ticket_number = db.Column(db.String(255), unique=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    subject = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(100), default='open')
    priority = db.Column(db.String(50), default='medium')
    category = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    resolved_at = db.Column(db.DateTime)
    assigned_to = db.Column(db.Integer, db.ForeignKey("user.user_id"))

    # Relationships
    user = db.relationship("User", back_populates="support_tickets", foreign_keys=[user_id])
    assigned_user = db.relationship("User", back_populates="assigned_tickets", foreign_keys=[assigned_to])
    support_messages = db.relationship("SupportMessage", back_populates="ticket", lazy="dynamic", cascade="all, delete-orphan")

    def __repr__(self):
        return f'<SupportTicket {self.ticket_number}>'


# -------------------------
# SUPPORT_MESSAGE
# -------------------------
class SupportMessage(db.Model):
    __tablename__ = "support_message"

    message_id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey("support_ticket.ticket_id"), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))
    message = db.Column(db.Text, nullable=False)
    sender_type = db.Column(db.String(50), nullable=False)  # 'customer' or 'support'
    sent_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    is_read = db.Column(db.Boolean, default=False, nullable=False)

    # Relationships
    ticket = db.relationship("SupportTicket", back_populates="support_messages")
    sender = db.relationship("User", back_populates="support_messages")

    def __repr__(self):
        return f'<SupportMessage ticket:{self.ticket_id}>'


# -------------------------
# PRODUCT_ANALYTIC
# -------------------------
class ProductAnalytic(db.Model):
    __tablename__ = "product_analytic"
    __table_args__ = (
        db.UniqueConstraint('product_id', 'year', 'month', name='uq_analytic_product_period'),
    )

    analytic_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.product_id"), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)  # 1-12
    total_sales = db.Column(db.Float, default=0)
    total_orders = db.Column(db.Integer, default=0)
    monthly_revenue = db.Column(db.Float, default=0)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    product = db.relationship("Product", back_populates="product_analytics")

    def __repr__(self):
        return f'<ProductAnalytic {self.product_id} {self.year}-{self.month:02d}>'


# -------------------------
# INVENTORY
# -------------------------
class Inventory(db.Model):
    __tablename__ = "inventory"

    inventory_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.product_id"), nullable=False)
    current_stock = db.Column(db.Integer, default=0, nullable=False)
    reorder_level = db.Column(db.Integer, default=10, nullable=False)
    max_capacity = db.Column(db.Integer, nullable=False)
    stock_status = db.Column(db.String(100), nullable=False)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_by = db.Column(db.Integer, db.ForeignKey("user.user_id"))

    # Relationships
    product = db.relationship("Product", back_populates="inventory_items")
    updated_by_user = db.relationship("User", back_populates="inventory_updates")
    stock_movements = db.relationship("StockMovement", back_populates="inventory", lazy="dynamic", cascade="all, delete-orphan")

    def needs_reorder(self):
        """Check if stock is below reorder level"""
        return self.current_stock <= self.reorder_level

    def update_stock_status(self):
        """Update stock status based on current stock"""
        if self.current_stock == 0:
            self.stock_status = 'out_of_stock'
        elif self.current_stock <= self.reorder_level:
            self.stock_status = 'low_stock'
        else:
            self.stock_status = 'in_stock'

    def __repr__(self):
        return f'<Inventory product:{self.product_id} stock:{self.current_stock}>'


# -------------------------
# PAYMENT
# -------------------------
class Payment(db.Model):
    __tablename__ = "payment"

    payment_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.order_id"), nullable=False)
    method = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(100), nullable=False)
    payment_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    transaction_id = db.Column(db.String(255))
    gateway = db.Column(db.String(255))
    gateway_response = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))

    # Relationships
    order = db.relationship("Order", back_populates="payments")
    user = db.relationship("User", back_populates="payments")

    def __repr__(self):
        return f'<Payment order:{self.order_id} status:{self.status}>'


# -------------------------
# ORDER_STATUS
# -------------------------
class OrderStatus(db.Model):
    __tablename__ = "order_status"

    status_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.order_id"), nullable=False)
    status = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_by = db.Column(db.Integer, db.ForeignKey("user.user_id"))

    # Relationships
    order = db.relationship("Order", back_populates="order_statuses")
    updated_by_user = db.relationship("User", back_populates="order_status_updates")

    def __repr__(self):
        return f'<OrderStatus order:{self.order_id} status:{self.status}>'


# -------------------------
# PETPAL_CONVERSATION
# -------------------------
class PetpalConversation(db.Model):
    __tablename__ = "petpal_conversation"

    conversation_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    pet_profile_id = db.Column(db.Integer, db.ForeignKey("pet_profile.pet_id"))
    pet_image_url = db.Column(db.String(500))
    detected_pet_type = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    last_message_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    # Relationships
    user = db.relationship("User", back_populates="petpal_conversations")
    pet_profile = db.relationship("PetProfile", back_populates="petpal_conversations")
    messages = db.relationship("PetpalMessage", back_populates="conversation", lazy="dynamic", cascade="all, delete-orphan")

    def __repr__(self):
        return f'<PetpalConversation {self.conversation_id}>'


# -------------------------
# PETPAL_MESSAGE
# -------------------------
class PetpalMessage(db.Model):
    __tablename__ = "petpal_message"

    message_id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey("petpal_conversation.conversation_id"), nullable=False)
    sender_type = db.Column(db.String(100), nullable=False)  # 'user' or 'ai'
    message_content = db.Column(db.Text, nullable=False)
    ai_recommendations = db.Column(db.Text)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    conversation = db.relationship("PetpalConversation", back_populates="messages")

    def __repr__(self):
        return f'<PetpalMessage conversation:{self.conversation_id} type:{self.sender_type}>'


# -------------------------
# CATEGORY
# -------------------------
class Category(db.Model):
    __tablename__ = "category"
    __table_args__ = (
        Index('idx_category_parent_active', 'parent_id', 'is_active'),
    )

    category_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False, index=True)
    slug = db.Column(db.String(255), unique=True, nullable=False, index=True)
    description = db.Column(db.Text)
    parent_id = db.Column(db.Integer, db.ForeignKey("category.category_id"))
    display_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    parent = db.relationship("Category", remote_side=[category_id], backref="children")
    products = db.relationship("Product", back_populates="category", lazy="dynamic")

    def __repr__(self):
        return f'<Category {self.name}>'


# -------------------------
# APP_SETTING
# -------------------------
class AppSetting(db.Model):
    __tablename__ = "app_setting"

    setting_id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(255), unique=True, nullable=False, index=True)
    value = db.Column(db.Text, nullable=False)
    group = db.Column(db.String(100), default='general', nullable=False)
    data_type = db.Column(db.String(50), default='string', nullable=False)  # string, number, boolean, json
    is_sensitive = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<AppSetting {self.key}>'


# -------------------------
# STOCK_MOVEMENT
# -------------------------
class StockMovement(db.Model):
    __tablename__ = "stock_movement"
    __table_args__ = (
        Index('idx_movement_product_time', 'product_id', 'created_at'),
    )

    movement_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.product_id"), nullable=False)
    inventory_id = db.Column(db.Integer, db.ForeignKey("inventory.inventory_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))
    movement_type = db.Column(db.String(50), nullable=False)  # in, out, adjust, return
    quantity_change = db.Column(db.Integer, nullable=False)
    reason = db.Column(db.String(255))
    reference_type = db.Column(db.String(100))  # order, purchase_order, manual
    reference_id = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    product = db.relationship("Product", back_populates="stock_movements")
    inventory = db.relationship("Inventory", back_populates="stock_movements")
    user = db.relationship("User", back_populates="stock_movements")

    def __repr__(self):
        return f'<StockMovement product:{self.product_id} qty:{self.quantity_change}>'


# -------------------------
# SHIPMENT
# -------------------------
class Shipment(db.Model):
    __tablename__ = "shipment"
    __table_args__ = (
        Index('idx_shipment_order_status', 'order_id', 'status'),
    )

    shipment_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.order_id"), nullable=False)
    carrier = db.Column(db.String(100))
    tracking_number = db.Column(db.String(255), index=True)
    status = db.Column(db.String(100), default='pending', nullable=False)
    shipped_at = db.Column(db.DateTime)
    delivered_at = db.Column(db.DateTime)
    notes = db.Column(db.Text)

    # Relationships
    order = db.relationship("Order", back_populates="shipments")

    def __repr__(self):
        return f'<Shipment order:{self.order_id} status:{self.status}>'


# -------------------------
# RETURN_REQUEST
# -------------------------
class ReturnRequest(db.Model):
    __tablename__ = "return_request"
    __table_args__ = (
        Index('idx_return_item_status', 'order_item_id', 'status'),
    )

    return_id = db.Column(db.Integer, primary_key=True)
    order_item_id = db.Column(db.Integer, db.ForeignKey("order_item.order_item_id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    reason = db.Column(db.String(500), nullable=False)
    status = db.Column(db.String(100), default='requested', nullable=False)  # requested, approved, rejected, refunded
    requested_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    processed_at = db.Column(db.DateTime)
    refund_amount = db.Column(db.Float, default=0)
    notes = db.Column(db.Text)

    # Relationships
    order_item = db.relationship("OrderItem", back_populates="return_requests")
    user = db.relationship("User", back_populates="return_requests")

    def __repr__(self):
        return f'<ReturnRequest item:{self.order_item_id} status:{self.status}>'


# -------------------------
# ADMIN_ACTIVITY_LOG
# -------------------------
class AdminActivityLog(db.Model):
    __tablename__ = "admin_activity_log"
    __table_args__ = (
        Index('idx_activity_user_time', 'user_id', 'created_at'),
    )

    log_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    action = db.Column(db.String(255), nullable=False)
    entity_type = db.Column(db.String(100))
    entity_id = db.Column(db.Integer)
    details = db.Column(db.Text)
    ip_address = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = db.relationship("User", back_populates="activity_logs")

    def __repr__(self):
        return f'<AdminActivityLog {self.action} by:{self.user_id}>'


# -------------------------
# SEARCH_QUERY_LOG
# -------------------------
class SearchQueryLog(db.Model):
    __tablename__ = "search_query_log"
    __table_args__ = (
        Index('idx_search_user_time', 'user_id', 'created_at'),
    )

    log_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))
    query_text = db.Column(db.String(1000), nullable=False)
    filters = db.Column(db.Text)
    results_count = db.Column(db.Integer, default=0)
    source = db.Column(db.String(100), default='web')  # web, admin, api
    ip_address = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = db.relationship("User", back_populates="search_logs")

    def __repr__(self):
        return f'<SearchQueryLog {self.query_text[:30]}>'