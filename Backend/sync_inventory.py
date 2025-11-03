from app import create_app
from models import db, Product, Inventory

def sync_inventory():
    """
    Sync all existing products with inventory records.
    Creates inventory records for products that don't have one.
    """
    print("Starting inventory sync...")
    
    # Get all products
    products = Product.query.all()
    print(f"Found {len(products)} products")
    
    # For each product, check if inventory exists and create if not
    created_count = 0
    for product in products:
        inventory = Inventory.query.filter_by(product_id=product.product_id).first()
        if not inventory:
            # Create inventory record
            inventory = Inventory(
                product_id=product.product_id,
                current_stock=product.stock,
                reorder_level=5,  # Default reorder level
                max_capacity=100,  # Default max capacity
                stock_status="in_stock" if product.stock > 10 else "low_stock" if product.stock > 0 else "out_of_stock"
            )
            db.session.add(inventory)
            created_count += 1
            print(f"Created inventory for product {product.product_id} ({product.name})")
    
    # Commit changes
    if created_count > 0:
        db.session.commit()
        print(f"Created {created_count} inventory records")
    else:
        print("No new inventory records needed")
    
    print("Inventory sync complete!")

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        sync_inventory()