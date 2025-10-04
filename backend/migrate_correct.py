#!/usr/bin/env python3
"""
Migration script to import existing catalog data from the original project
"""

import os
import json
import sqlite3
import csv
from pathlib import Path
import sys

def migrate_existing_data():
    """Migrate existing catalog data to the new database"""
    print("Migrating existing catalog data...")
    
    # Check if output directory exists
    output_dir = Path("../output")
    if not output_dir.exists():
        print("ERROR: Output directory not found. Please run the original catalog generator first.")
        return False
    
    # Check if catalog.csv exists
    csv_file = output_dir / "catalog.csv"
    if not csv_file.exists():
        print("ERROR: catalog.csv not found. Please run the original catalog generator first.")
        return False
    
    # Initialize database (use root directory path)
    db_path = "../catalog.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Clear existing data
    cursor.execute("DELETE FROM products")
    
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
    print("Reading existing catalog data...")
    products_imported = 0
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                # Extract data from CSV row
                article = row.get('article', '').strip()
                colour = row.get('colour', '').strip()
                size = row.get('size', '').strip()
                pair = row.get('pair', '').strip()
                
                # Try to extract price from rate_row if available
                price = None
                rate_row = row.get('rate_row', '')
                if rate_row and rate_row != 'None':
                    try:
                        # Parse the rate_row JSON to extract price
                        import ast
                        rate_data = ast.literal_eval(rate_row)
                        if isinstance(rate_data, dict) and 'col_2' in rate_data:
                            price = rate_data['col_2']
                    except:
                        pass
                
                # Skip empty or invalid entries
                if not article or article == '' or article.startswith('-'):
                    continue
                
                # Insert product with current timestamp
                from datetime import datetime
                now = datetime.utcnow()
                cursor.execute("""
                    INSERT INTO products (article, colour, size, pair, price, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (article, colour, size, pair, price, now, now))
                
                products_imported += 1
        
        conn.commit()
        print(f"SUCCESS: Imported {products_imported} products from CSV")
        
    except Exception as e:
        print(f"ERROR: Error reading CSV: {e}")
        return False
    
    # Show summary
    cursor.execute("SELECT COUNT(*) FROM products")
    total_products = cursor.fetchone()[0]
    
    print("\nMigration Summary:")
    print(f"   Total products: {total_products}")
    
    # Show some sample products
    cursor.execute("SELECT article, colour, size, pair, price FROM products LIMIT 5")
    sample_products = cursor.fetchall()
    print("\nSample products:")
    for product in sample_products:
        print(f"   Article: {product[0]}, Colour: {product[1]}, Size: {product[2]}, Pair: {product[3]}, Price: {product[4]}")
    
    conn.close()
    
    print("\nMigration completed!")
    print("\nNext steps:")
    print("1. Start your application server")
    print("2. View the catalog at http://localhost:8000")
    print("3. Use the admin panel at http://localhost:8000/admin to manage products")
    
    return True

def main():
    """Main function"""
    print("Ciffox Catalog Data Migration")
    print("=" * 40)
    
    if migrate_existing_data():
        print("\nMigration completed successfully!")
    else:
        print("\nMigration failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
