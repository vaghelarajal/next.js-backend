"""
Migration script to seed initial product data
"""
from sqlalchemy.orm import Session
from models import Product
from config.database import SessionLocal


def get_dummy_products():
    """Return list of dummy product data"""
    return [
        {
            "name": "Wireless Bluetooth Headphones",
            "description": "High-quality wireless headphones with noise cancellation and 30-hour battery life.",
            "price": 99.99,
            "category": "Electronics",
            "stock_quantity": 50,
            "is_active": True
        },
        {
            "name": "Organic Cotton T-Shirt",
            "description": "Comfortable 100% organic cotton t-shirt available in multiple colors.",
            "price": 24.99,
            "category": "Clothing",
            "stock_quantity": 100,
            "is_active": True
        },
        {
            "name": "Stainless Steel Water Bottle",
            "description": "Insulated water bottle that keeps drinks cold for 24 hours or hot for 12 hours.",
            "price": 34.99,
            "category": "Home & Garden",
            "stock_quantity": 75,
            "is_active": True
        },
        {
            "name": "Yoga Mat Premium",
            "description": "Non-slip yoga mat made from eco-friendly materials, perfect for all yoga practices.",
            "price": 49.99,
            "category": "Sports & Fitness",
            "stock_quantity": 30,
            "is_active": True
        },
        {
            "name": "Coffee Maker Deluxe",
            "description": "Programmable coffee maker with built-in grinder and thermal carafe.",
            "price": 149.99,
            "category": "Kitchen",
            "stock_quantity": 20,
            "is_active": True
        },
        {
            "name": "LED Desk Lamp",
            "description": "Adjustable LED desk lamp with USB charging port and touch controls.",
            "price": 39.99,
            "category": "Office",
            "stock_quantity": 40,
            "is_active": True
        },
        {
            "name": "Wireless Phone Charger",
            "description": "Fast wireless charging pad compatible with all Qi-enabled devices.",
            "price": 29.99,
            "category": "Electronics",
            "stock_quantity": 60,
            "is_active": True
        },
        {
            "name": "Running Shoes",
            "description": "Lightweight running shoes with advanced cushioning and breathable mesh upper.",
            "price": 89.99,
            "category": "Sports & Fitness",
            "stock_quantity": 45,
            "is_active": True
        },
        {
            "name": "Ceramic Dinner Set",
            "description": "16-piece ceramic dinner set including plates, bowls, and mugs for 4 people.",
            "price": 79.99,
            "category": "Kitchen",
            "stock_quantity": 25,
            "is_active": True
        },
        {
            "name": "Bluetooth Speaker",
            "description": "Portable Bluetooth speaker with 360-degree sound and waterproof design.",
            "price": 59.99,
            "category": "Electronics",
            "stock_quantity": 35,
            "is_active": True
        }
    ]


def seed_products():
    """
    Seed the database with initial product data.
    Only runs if the products table is empty.
    """
    print("Checking products table...")
    
    db = SessionLocal()
    try:
        # Check if products table has any records
        existing_count = db.query(Product).count()
        
        if existing_count > 0:
            print(f"Products table already has {existing_count} records. Skipping seed.")
            return False
        
        print("Products table is empty. Inserting dummy data...")
        
        # Get dummy products
        dummy_products = get_dummy_products()
        
        # Insert each product
        for product_data in dummy_products:
            product = Product(**product_data)
            db.add(product)
        
        # Commit all products
        db.commit()
        
        print(f"Successfully inserted {len(dummy_products)} products!")
        return True
        
    except Exception as e:
        print(f"Error seeding products: {e}")
        db.rollback()
        return False
    finally:
        db.close()


def run_migrations():
    """
    Run all migration scripts.
    This function is called when the app starts.
    """
    print("\n" + "=" * 60)
    print("RUNNING DATABASE MIGRATIONS")
    print("=" * 60)
    
    try:
        # Run product seeding
        seed_products()
        
        print("=" * 60)
        print("MIGRATIONS COMPLETED SUCCESSFULLY")
        print("=" * 60 + "\n")
        
    except Exception as e:
        print(f"MIGRATION FAILED: {e}")
        print("=" * 60 + "\n")