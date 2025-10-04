#!/usr/bin/env python3
"""
Script to update product images in the database
"""

import sqlite3
import os
from pathlib import Path

def update_product_images():
    """Update product images in the database"""
    print("Updating product images...")
    
    # Connect to database
    db_path = "../catalog.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all products
    cursor.execute("SELECT id, article FROM products ORDER BY id")
    products = cursor.fetchall()
    
    # Get available images
    thumbs_dir = Path("../output/thumbs")
    available_images = list(thumbs_dir.glob("*.jpg"))
    
    print(f"Found {len(products)} products and {len(available_images)} images")
    
    # Update products with images (cycle through available images)
    updated_count = 0
    for i, (product_id, article) in enumerate(products):
        if i < len(available_images):
            image_name = available_images[i].name
            image_url = f"/static/{image_name}"
            
            # Copy image to static directory if not already there
            static_path = Path(f"static/{image_name}")
            if not static_path.exists():
                import shutil
                shutil.copy2(available_images[i], static_path)
            
            # Update database
            cursor.execute("""
                UPDATE products 
                SET image_url = ? 
                WHERE id = ?
            """, (image_url, product_id))
            
            updated_count += 1
            print(f"Updated product {product_id} ({article}) with image {image_name}")
    
    conn.commit()
    conn.close()
    
    print(f"Successfully updated {updated_count} products with images")
    return True

def main():
    """Main function"""
    print("Product Image Update")
    print("=" * 30)
    
    if update_product_images():
        print("\nImage update completed successfully!")
    else:
        print("\nImage update failed!")

if __name__ == "__main__":
    main()
