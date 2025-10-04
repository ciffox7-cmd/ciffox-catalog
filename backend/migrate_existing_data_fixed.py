#!/usr/bin/env python3
"""
Migration script to import existing catalog data from the original project
"""

import os
import json
import sqlite3
from pathlib import Path
import sys

def migrate_existing_data():
    """Migrate existing catalog data to the new database"""
    print("🔄 Migrating existing catalog data...")
    
    # Check if output directory exists
    output_dir = Path("../output")
    if not output_dir.exists():
        print("❌ Output directory not found. Please run the original catalog generator first.")
        return False
    
    # Check if catalog.csv exists
    csv_file = output_dir / "catalog.csv"
    if not csv_file.exists():
        print("❌ catalog.csv not found. Please run the original catalog generator first.")
        return False
    
    # Check if OCR directory exists
    ocr_dir = output_dir / "ocr"
    if not ocr_dir.exists():
        print("❌ OCR directory not found. Please run the original catalog generator first.")
        return False
    
    # Initialize database
    db_path = "catalog.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create products table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            article TEXT,
            colour TEXT,
            size TEXT,
            pair TEXT,
            price TEXT,
            image_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Read existing CSV data
    print("📖 Reading existing catalog data...")
    products_imported = 0
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Skip header
        for line in lines[1:]:
            parts = line.strip().split(',')
            if len(parts) >= 4:
                article = parts[0].strip('"')
                colour = parts[1].strip('"')
                size = parts[2].strip('"')
                pair = parts[3].strip('"')
                price = parts[4].strip('"') if len(parts) > 4 else None
                
                # Check if product already exists
                cursor.execute("SELECT id FROM products WHERE article = ?", (article,))
                if cursor.fetchone():
                    continue
                
                # Insert product
                cursor.execute("""
                    INSERT INTO products (article, colour, size, pair, price)
                    VALUES (?, ?, ?, ?, ?)
                """, (article, colour, size, pair, price))
                
                products_imported += 1
        
        conn.commit()
        print(f"✅ Imported {products_imported} products from CSV")
        
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        return False
    
    # Try to import image URLs from OCR files
    print("🖼️  Processing image URLs...")
    images_processed = 0
    
    try:
        for ocr_file in ocr_dir.glob("*.json"):
            try:
                with open(ocr_file, 'r', encoding='utf-8') as f:
                    ocr_data = json.load(f)
                
                # Extract image path from OCR data
                image_path = ocr_data.get('image_path', '')
                if image_path:
                    # Convert to Google Drive URL format
                    # This is a placeholder - you'll need to upload images to Google Drive
                    # and update the URLs accordingly
                    image_name = Path(image_path).name
                    google_drive_url = f"https://drive.google.com/uc?id=PLACEHOLDER_{image_name}"
                    
                    # Find matching product by article name
                    article_name = ocr_data.get('article', '')
                    if article_name:
                        cursor.execute("""
                            UPDATE products 
                            SET image_url = ? 
                            WHERE article = ? AND image_url IS NULL
                        """, (google_drive_url, article_name))
                        
                        if cursor.rowcount > 0:
                            images_processed += 1
            except Exception as e:
                print(f"⚠️  Warning: Could not process {ocr_file}: {e}")
                continue
        
        conn.commit()
        print(f"✅ Processed {images_processed} image references")
        
    except Exception as e:
        print(f"⚠️  Warning: Could not process image URLs: {e}")
    
    # Show summary
    cursor.execute("SELECT COUNT(*) FROM products")
    total_products = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM products WHERE image_url IS NOT NULL")
    products_with_images = cursor.fetchone()[0]
    
    print("\n📊 Migration Summary:")
    print(f"   Total products: {total_products}")
    print(f"   Products with images: {products_with_images}")
    print(f"   Products without images: {total_products - products_with_images}")
    
    conn.close()
    
    print("\n✅ Migration completed!")
    print("\n📋 Next steps:")
    print("1. Upload your product images to Google Drive")
    print("2. Update the image URLs in the database")
    print("3. Deploy your application to Fly.io")
    
    return True

def main():
    """Main function"""
    print("🔄 Ciffox Catalog Data Migration")
    print("=" * 40)
    
    if migrate_existing_data():
        print("\n🎉 Migration completed successfully!")
    else:
        print("\n❌ Migration failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
