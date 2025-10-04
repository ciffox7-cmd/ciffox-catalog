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
    print("Reading existing catalog data...")
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
        print(f"SUCCESS: Imported {products_imported} products from CSV")
        
    except Exception as e:
        print(f"ERROR: Error reading CSV: {e}")
        return False
    
    # Show summary
    cursor.execute("SELECT COUNT(*) FROM products")
    total_products = cursor.fetchone()[0]
    
    print("\nMigration Summary:")
    print(f"   Total products: {total_products}")
    
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
