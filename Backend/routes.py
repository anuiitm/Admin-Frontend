import os
from flask import Blueprint, request, current_app
from sqlalchemy import func
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename

from models import db, User, Product, Category, Inventory, Order, OrderItem, OrderStatus, Shipment, PromoCode, FAQ, AppSetting, StockMovement, ProductAnalytic, DashboardReport, SearchQueryLog, ReturnRequest, Notification


api_bp = Blueprint("api", __name__)


def ok(data=None, status=200):
    return (data or {"ok": True}, status)


def parse_iso_datetime(value):
    if not value:
        return None
    try:
        # Accept ISO strings with 'Z' timezone by converting to +00:00
        return datetime.fromisoformat(value.replace('Z', '+00:00'))
    except Exception:
        return None


@api_bp.get("/health")
def api_health():
    return ok({"status": "ok"})


# -------- Auth (placeholder minimal) --------
@api_bp.post("/auth/login")
def login():
    body = request.get_json(force=True, silent=True) or {}
    email = body.get("email")
    password = body.get("password")
    if not email or not password:
        return ({"error": "email and password required"}, 400)
    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return ({"error": "invalid credentials"}, 401)
    return ok({"user_id": user.user_id, "is_admin": user.is_admin})


# -------- Users (list for Customers page) --------
@api_bp.get("/users")
def list_users():
    users = User.query.order_by(User.date_joined.desc()).all()
    return ok([
        {
            "user_id": u.user_id,
            "full_name": u.full_name,
            "email": u.email,
            "phone": u.phone,
            "is_admin": u.is_admin,
            "is_active": u.is_active,
            "date_joined": u.date_joined.isoformat(),
        }
        for u in users
    ])


# -------- Categories --------
@api_bp.get("/categories")
def get_categories():
    cats = Category.query.order_by(Category.display_order.asc(), Category.name.asc()).all()
    return ok([
        {
            "category_id": c.category_id,
            "name": c.name,
            "slug": c.slug,
            "parent_id": c.parent_id,
            "is_active": c.is_active,
        }
        for c in cats
    ])


@api_bp.post("/categories")
def create_category():
    body = request.get_json(force=True, silent=True) or {}
    c = Category(
        name=body.get("name"),
        slug=body.get("slug"),
        description=body.get("description"),
        parent_id=body.get("parent_id"),
        display_order=body.get("display_order", 0),
        is_active=body.get("is_active", True),
    )
    db.session.add(c)
    db.session.commit()
    return ok({"category_id": c.category_id}, 201)


@api_bp.put("/categories/<int:category_id>")
def update_category(category_id):
    body = request.get_json(force=True, silent=True) or {}
    c = Category.query.get_or_404(category_id)
    for field in ["name", "slug", "description", "parent_id", "display_order", "is_active"]:
        if field in body:
            setattr(c, field, body[field])
    db.session.commit()
    return ok({"category_id": c.category_id})


@api_bp.delete("/categories/<int:category_id>")
def delete_category(category_id):
    c = Category.query.get_or_404(category_id)
    db.session.delete(c)
    db.session.commit()
    return ok()


# -------- Products --------
@api_bp.get("/products")
def list_products():
    products = Product.query.order_by(Product.created_at.desc()).all()
    return ok([
        {
            "product_id": p.product_id,
            "name": p.name,
            "description": p.description,
            "sku": p.sku,
            "price": p.price,
            "discount_price": p.discount_price,
            "stock": p.stock,            
            "main_image_url": p.main_image_url,
            "tags": p.tags.split(",") if p.tags else [],
            "category_name": p.category_name,
            "category_id": p.category_id,
            "pet_type": p.pet_type,            
            "status": p.status,
            "is_active": p.is_active,
            "is_featured": p.is_featured,
            "created_at": p.created_at.isoformat(),
        }
        for p in products
    ])

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@api_bp.post("/upload-product-image")
def upload_image():
    if 'image' not in request.files:
        return {"error": "No file found"}, 400

    file = request.files['image']

    if file.filename == '':
        return {"error": "File name missing"}, 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        upload_folder = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)

        file_url = f"/static/uploads/{filename}"
        return {"message": "Uploaded successfully", "url": file_url}, 201
    return {"error": "Invalid file type"}, 400

@api_bp.post("/products")
def create_product():
    body = request.get_json(force=True, silent=True) or {}
    required = ["name", "sku", "price", "category_name", "pet_type"]
    missing = [f for f in required if not body.get(f)]
    if missing:
        return ({"error": f"Missing required fields: {', '.join(missing)}"}, 400)

    # Fallback image if none provided
    main_image_url = body.get("main_image_url") or "/paws.png"

    try:
        p = Product(
            name=body.get("name"),
            sku=body.get("sku"),
            description=body.get("description"),
            short_description=body.get("short_description"),
            price=body.get("price", 0),
            discount_price=body.get("discount_price"),
            stock=body.get("stock", 0),
            main_image_url=main_image_url,
            weight=body.get("weight"),
            dimensions=body.get("dimensions"),
            tags=",".join(body.get("tags")) if isinstance(body.get("tags"), list) else body.get("tags"),
            category_name=body.get("category_name") or "",
            pet_type=body.get("pet_type") or "general",
            uploader_id=body.get("uploader_id"),
            is_active=body.get("is_active", True),
            is_featured=body.get("is_featured", False),
            ingredients=body.get("ingredients"),
            features=body.get("features"),
            status=body.get("status", "active"),
            category_id=body.get("category_id"),
        )
        db.session.add(p)
        db.session.commit()
        return ok({"product_id": p.product_id}, 201)
    except IntegrityError as e:
        db.session.rollback()
        return ({"error": "SKU must be unique"}, 400)
    except Exception as e:
        db.session.rollback()
        return ({"error": str(e)}, 500)


@api_bp.put("/products/<int:product_id>")
def update_product(product_id):
    body = request.get_json(force=True, silent=True) or {}
    p = Product.query.get_or_404(product_id)
    updatable = [
        "name","sku","description","short_description","price","discount_price","stock",
        "main_image_url","weight","dimensions","tags","category_name","pet_type","uploader_id",
        "is_active","is_featured","ingredients","features","status","category_id"
    ]
    for field in updatable:
        if field in body:
            if field == "tags" and isinstance(body[field], list):
                # convert array → comma-separated string
                setattr(p, field, ",".join(body[field]))
            else:
                setattr(p, field, body[field])
    db.session.commit()
    return ok({"product_id": p.product_id})


@api_bp.delete("/products/<int:product_id>")
def delete_product(product_id):
    p = Product.query.get_or_404(product_id)
    for inv in p.inventory_items:
        db.session.delete(inv)
    db.session.delete(p)
    db.session.commit()
    return ok()


# -------- Inventory --------
@api_bp.get("/inventory")
def list_inventory():
    items = Inventory.query.all()
    return ok([
        {
            "inventory_id": i.inventory_id,
            "product_id": i.product_id,
            "current_stock": i.current_stock,
            "reorder_level": i.reorder_level,
            "max_capacity": i.max_capacity,
            "stock_status": i.stock_status,
        }
        for i in items
    ])


@api_bp.post("/inventory/adjust")
def adjust_inventory():
    body = request.get_json(force=True, silent=True) or {}
    inventory_id = body.get("inventory_id")
    quantity_change = int(body.get("quantity_change", 0))
    reason = body.get("reason")
    user_id = body.get("user_id")

    inv = Inventory.query.get_or_404(inventory_id)
    inv.current_stock = (inv.current_stock or 0) + quantity_change
    inv.update_stock_status()

    movement = StockMovement(
        product_id=inv.product_id,
        inventory_id=inv.inventory_id,
        user_id=user_id,
        movement_type="adjust",
        quantity_change=quantity_change,
        reason=reason,
        created_at=datetime.utcnow(),
    )
    db.session.add(movement)
    db.session.commit()
    return ok({"inventory_id": inv.inventory_id, "current_stock": inv.current_stock})


# -------- Orders, Status, Shipments --------
@api_bp.get("/orders")
def list_orders():
    orders = Order.query.order_by(Order.order_date.desc()).all()
    return ok([
        {
            "order_id": o.order_id,
            "order_number": o.order_number,
            "user_id": o.user_id,
            "order_status": o.order_status,
            "payment_status": o.payment_status,
            "total_price": o.total_price,
            "order_date": o.order_date.isoformat(),
        }
        for o in orders
    ])


@api_bp.get("/orders/<int:order_id>")
def get_order(order_id):
    o = Order.query.get_or_404(order_id)
    return ok({
        "order_id": o.order_id,
        "order_number": o.order_number,
        "user_id": o.user_id,
        "status": o.order_status,
        "items": [
            {
                "order_item_id": i.order_item_id,
                "product_id": i.product_id,
                "product_name": i.product_name,
                "quantity": i.quantity,
                "price_at_purchase": i.price_at_purchase,
                "total_price": i.total_price,
            }
            for i in o.order_items
        ],
        "shipments": [
            {
                "shipment_id": s.shipment_id,
                "carrier": s.carrier,
                "tracking_number": s.tracking_number,
                "status": s.status,
                "shipped_at": s.shipped_at.isoformat() if s.shipped_at else None,
                "delivered_at": s.delivered_at.isoformat() if s.delivered_at else None,
            }
            for s in o.shipments
        ]
    })


@api_bp.post("/orders/<int:order_id>/status")
def update_order_status(order_id):
    body = request.get_json(force=True, silent=True) or {}
    status = body.get("status")
    description = body.get("description")
    updated_by = body.get("updated_by")

    o = Order.query.get_or_404(order_id)
    o.order_status = status or o.order_status

    st = OrderStatus(order_id=o.order_id, status=status or o.order_status, description=description, updated_by=updated_by)
    db.session.add(st)
    db.session.commit()
    return ok({"order_id": o.order_id, "order_status": o.order_status})


@api_bp.post("/orders/<int:order_id>/shipments")
def create_shipment(order_id):
    body = request.get_json(force=True, silent=True) or {}
    o = Order.query.get_or_404(order_id)
    s = Shipment(
        order_id=o.order_id,
        carrier=body.get("carrier"),
        tracking_number=body.get("tracking_number"),
        status=body.get("status", "pending"),
        shipped_at=datetime.utcnow() if body.get("status") == "shipped" else None,
        notes=body.get("notes"),
    )
    db.session.add(s)
    db.session.commit()
    return ok({"shipment_id": s.shipment_id}, 201)


# -------- Promo Codes --------
@api_bp.get("/promos")
def list_promos():
    promos = PromoCode.query.order_by(PromoCode.created_at.desc()).all()
    return ok([
        {
            "promo_id": p.promo_id,
            "code": p.code,
            "name": p.name,
            "discount_type": p.discount_type,
            "discount_value": p.discount_value,
            "valid_from": p.valid_from.isoformat(),
            "valid_until": p.valid_until.isoformat(),
            "active": p.active,
        }
        for p in promos
    ])


@api_bp.post("/promos")
def create_promo():
    body = request.get_json(force=True, silent=True) or {}
    required = ["code", "discount_type", "discount_value", "valid_from", "valid_until"]
    missing = [f for f in required if body.get(f) in (None, "")]
    if missing:
        return ({"error": f"Missing required fields: {', '.join(missing)}"}, 400)
    if body.get("discount_type") not in ("percentage", "fixed"):
        return ({"error": "discount_type must be 'percentage' or 'fixed'"}, 400)
    try:
        p = PromoCode(
            code=body.get("code"),
            name=body.get("name") or body.get("code"),
            description=body.get("description"),
            discount_type=body.get("discount_type"),
            discount_value=body.get("discount_value", 0),
            min_order_value=body.get("min_order_value", 0),
            max_discount_amount=body.get("max_discount_amount"),
            valid_from=parse_iso_datetime(body.get("valid_from")) or datetime.utcnow(),
            valid_until=parse_iso_datetime(body.get("valid_until")) or datetime.utcnow(),
            max_uses=body.get("max_uses"),
            max_uses_per_user=body.get("max_uses_per_user", 1),
            active=body.get("active", True),
            created_by=body.get("created_by"),
        )
        db.session.add(p)
        db.session.commit()
        return ok({"promo_id": p.promo_id}, 201)
    except IntegrityError:
        db.session.rollback()
        return ({"error": "Promo code must be unique"}, 400)
    except Exception as e:
        db.session.rollback()
        return ({"error": str(e)}, 500)


@api_bp.put("/promos/<int:promo_id>")
def update_promo(promo_id):
    body = request.get_json(force=True, silent=True) or {}
    p = PromoCode.query.get_or_404(promo_id)
    fields = [
        "code","name","description","discount_type","discount_value","min_order_value",
        "max_discount_amount","valid_from","valid_until","max_uses","max_uses_per_user","active"
    ]
    for f in fields:
        if f in body:
            if f in ("valid_from", "valid_until"):
                setattr(p, f, parse_iso_datetime(body[f]) or getattr(p, f))
            else:
                setattr(p, f, body[f])
    db.session.commit()
    return ok({"promo_id": p.promo_id})


@api_bp.delete("/promos/<int:promo_id>")
def delete_promo(promo_id):
    p = PromoCode.query.get_or_404(promo_id)
    db.session.delete(p)
    db.session.commit()
    return ok()


# -------- FAQ --------
@api_bp.get("/faqs")
def list_faqs():
    faqs = FAQ.query.order_by(FAQ.display_order.asc(), FAQ.created_at.desc()).all()
    return ok([
        {
            "faq_id": f.faq_id,
            "question": f.question,
            "answer": f.answer,
            "category": f.category,
            "display_order": f.display_order,
            "is_active": f.is_active,
        }
        for f in faqs
    ])


@api_bp.post("/faqs")
def create_faq():
    body = request.get_json(force=True, silent=True) or {}
    required = ["question", "answer", "category"]
    missing = [f for f in required if not (body.get(f) and str(body.get(f)).strip())]
    if missing:
        return ({"error": f"Missing required fields: {', '.join(missing)}"}, 400)
    try:
        f = FAQ(
            question=body.get("question").strip(),
            answer=body.get("answer").strip(),
            category=body.get("category").strip(),
            display_order=body.get("display_order", 0),
            is_active=body.get("is_active", True),
            created_by=body.get("created_by"),
        )
        db.session.add(f)
        db.session.commit()
        return ok({"faq_id": f.faq_id}, 201)
    except Exception as e:
        db.session.rollback()
        return ({"error": str(e)}, 500)


@api_bp.put("/faqs/<int:faq_id>")
def update_faq(faq_id):
    body = request.get_json(force=True, silent=True) or {}
    f = FAQ.query.get_or_404(faq_id)
    for field in ["question", "answer", "category", "display_order", "is_active"]:
        if field in body:
            setattr(f, field, body[field])
    db.session.commit()
    return ok({"faq_id": f.faq_id})


@api_bp.delete("/faqs/<int:faq_id>")
def delete_faq(faq_id):
    f = FAQ.query.get_or_404(faq_id)
    db.session.delete(f)
    db.session.commit()
    return ok()


# -------- Settings (AppSetting) --------
@api_bp.get("/settings")
def list_settings():
    settings = AppSetting.query.order_by(AppSetting.group.asc(), AppSetting.key.asc()).all()
    return ok([
        {
            "setting_id": s.setting_id,
            "key": s.key,
            "value": s.value,
            "group": s.group,
            "data_type": s.data_type,
            "is_sensitive": s.is_sensitive,
        }
        for s in settings
    ])


@api_bp.post("/settings")
def create_setting():
    body = request.get_json(force=True, silent=True) or {}
    s = AppSetting(
        key=body.get("key"),
        value=body.get("value", ""),
        group=body.get("group", "general"),
        data_type=body.get("data_type", "string"),
        is_sensitive=body.get("is_sensitive", False),
    )
    db.session.add(s)
    db.session.commit()
    return ok({"setting_id": s.setting_id}, 201)


@api_bp.put("/settings/<int:setting_id>")
def update_setting(setting_id):
    body = request.get_json(force=True, silent=True) or {}
    s = AppSetting.query.get_or_404(setting_id)
    for field in ["key", "value", "group", "data_type", "is_sensitive"]:
        if field in body:
            setattr(s, field, body[field])
    db.session.commit()
    return ok({"setting_id": s.setting_id})


@api_bp.delete("/settings/<int:setting_id>")
def delete_setting(setting_id):
    s = AppSetting.query.get_or_404(setting_id)
    db.session.delete(s)
    db.session.commit()
    return ok()


# -------- Dashboard / Analysis --------
@api_bp.get("/dashboard/summary")
def dashboard_summary():
    # Simple live summary; can be replaced with precomputed DashboardReport
    total_sales = db.session.query(func.sum(Order.total_price)).scalar() or 0
    total_orders = db.session.query(func.count(Order.order_id)).scalar() or 0
    total_customers = db.session.query(func.count(User.user_id)).scalar() or 0
    low_stock = db.session.query(func.count(Inventory.inventory_id)).filter(Inventory.stock_status != 'in_stock').scalar() or 0
    return ok({
        "total_sales": total_sales,
        "total_orders": total_orders,
        "total_customers": total_customers,
        "low_stock_products": low_stock,
    })


@api_bp.get("/analysis/products")
def analysis_products():
    analytics = ProductAnalytic.query.order_by(ProductAnalytic.year.desc(), ProductAnalytic.month.desc()).limit(100).all()
    return ok([
        {
            "product_id": a.product_id,
            "year": a.year,
            "month": a.month,
            "total_sales": a.total_sales,
            "total_orders": a.total_orders,
            "monthly_revenue": a.monthly_revenue,
        }
        for a in analytics
    ])


# -------- Search logging (optional) --------
@api_bp.post("/search/log")
def log_search():
    body = request.get_json(force=True, silent=True) or {}
    log = SearchQueryLog(
        user_id=body.get("user_id"),
        query_text=body.get("query_text", ""),
        filters=body.get("filters"),
        results_count=body.get("results_count", 0),
        source=body.get("source", "admin"),
        ip_address=request.remote_addr,
    )
    db.session.add(log)
    db.session.commit()
    return ok({"log_id": log.log_id}, 201)


# -------- Notifications (basic) --------
@api_bp.get("/notifications")
def list_notifications():
    user_id = request.args.get("user_id", type=int)
    q = Notification.query
    if user_id:
        q = q.filter(Notification.user_id == user_id)
    notes = q.order_by(Notification.created_at.desc()).limit(100).all()
    return ok([
        {
            "notification_id": n.notification_id,
            "user_id": n.user_id,
            "title": n.title,
            "message": n.message,
            "type": n.type,
            "link": n.link,
            "is_read": n.is_read,
            "created_at": n.created_at.isoformat(),
        }
        for n in notes
    ])


@api_bp.post("/notifications/<int:notification_id>/read")
def mark_notification_read(notification_id):
    n = Notification.query.get_or_404(notification_id)
    n.mark_as_read()
    db.session.commit()
    return ok({"notification_id": n.notification_id, "is_read": n.is_read})



