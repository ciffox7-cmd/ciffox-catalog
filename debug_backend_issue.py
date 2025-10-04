#!/usr/bin/env python3
"""
Debug the backend 500 error by testing the database and model directly
"""

import sys
import os
sys.path.insert(0, 'backend')

def test_database_and_model():
    """Test database connection and Product model"""
    try:
        from main import Product, SessionLocal, get_db
        print("OK: Imports successful")
        
        # Test database session
        db = SessionLocal()
        print("OK: Database session created")
        
        # Test query
        products = db.query(Product).limit(5).all()
        print(f"OK: Query successful: {len(products)} products found")
        
        # Test individual product attributes
        if products:
            product = products[0]
            print(f"Sample product attributes:")
            print(f"  ID: {product.id}")
            print(f"  Article: {product.article}")
            print(f"  Colour: {product.colour}")
            print(f"  Size: {product.size}")
            print(f"  Pair: {product.pair}")
            print(f"  Price: {product.price}")
            print(f"  Image URL: {product.image_url}")
        
        db.close()
        print("OK: Database connection closed")
        
        # Test the get_db dependency
        print("\nTesting get_db dependency...")
        db_gen = get_db()
        db = next(db_gen)
        print("OK: get_db dependency works")
        
        # Test query through dependency
        products = db.query(Product).limit(3).all()
        print(f"OK: Query through dependency: {len(products)} products")
        
        db.close()
        print("OK: All tests passed!")
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_database_and_model()
