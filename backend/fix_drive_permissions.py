#!/usr/bin/env python3
"""
Script to fix Google Drive permissions and update image URLs
"""

import os
import sqlite3
import json
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Scopes required for the application
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def fix_drive_permissions():
    """Fix Google Drive permissions and update image URLs"""
    print("Fixing Google Drive permissions...")
    
    # Load credentials
    creds = None
    token_file = 'token.json'
    
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            print("ERROR: No valid credentials found. Please run setup_google_drive_simple.py first.")
            return False
    
    # Create Drive service
    try:
        service = build('drive', 'v3', credentials=creds)
        print("SUCCESS: Google Drive service created")
        
        # Get folder ID from .env file
        folder_id = None
        if os.path.exists('.env'):
            with open('.env', 'r') as f:
                for line in f:
                    if line.startswith('GOOGLE_DRIVE_FOLDER_ID='):
                        folder_id = line.split('=')[1].strip()
                        break
        
        if not folder_id:
            print("ERROR: Google Drive folder ID not found in .env file")
            return False
        
        print(f"Using folder ID: {folder_id}")
        
        # Connect to database
        db_path = "catalog.db"
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all products with their current image URLs
        cursor.execute("SELECT id, article, image_url FROM products WHERE image_url IS NOT NULL ORDER BY id")
        products = cursor.fetchall()
        
        print(f"Found {len(products)} products to fix")
        
        fixed_count = 0
        
        for product_id, article, current_url in products:
            print(f"Processing product {product_id} ({article})")
            
            try:
                # Extract file ID from current URL
                if 'id=' in current_url:
                    file_id = current_url.split('id=')[1]
                else:
                    print(f"WARNING: Could not extract file ID from URL: {current_url}")
                    continue
                
                # Get file details
                file_info = service.files().get(fileId=file_id, fields='id,name,webViewLink').execute()
                
                # Make file publicly accessible
                try:
                    service.permissions().create(
                        fileId=file_id,
                        body={'role': 'reader', 'type': 'anyone'}
                    ).execute()
                    print(f"SUCCESS: Made file {file_id} publicly accessible")
                except HttpError as e:
                    if e.resp.status == 409:  # Permission already exists
                        print(f"INFO: File {file_id} already has public access")
                    else:
                        print(f"WARNING: Could not make file {file_id} public: {e}")
                
                # Update with the correct public URL format
                new_url = f"https://drive.google.com/uc?export=view&id={file_id}"
                
                # Update database
                cursor.execute("""
                    UPDATE products 
                    SET image_url = ? 
                    WHERE id = ?
                """, (new_url, product_id))
                
                fixed_count += 1
                print(f"SUCCESS: Updated product {product_id} with new URL")
                
            except HttpError as e:
                print(f"ERROR: Failed to process file for product {product_id}: {e}")
                continue
            except Exception as e:
                print(f"ERROR: Unexpected error for product {product_id}: {e}")
                continue
        
        conn.commit()
        conn.close()
        
        print(f"\nFix Summary:")
        print(f"Products processed: {fixed_count}")
        print(f"Total products: {len(products)}")
        
        return True
        
    except Exception as e:
        print(f"ERROR: Failed to create Google Drive service: {e}")
        return False

def main():
    """Main function"""
    print("Ciffox Catalog - Fix Google Drive Permissions")
    print("=" * 50)
    
    if fix_drive_permissions():
        print("\nSUCCESS: Google Drive permissions fixed!")
        print("\nNext steps:")
        print("1. Restart your application server")
        print("2. Check the catalog to see if images load correctly")
        print("3. Test a few image URLs manually in your browser")
    else:
        print("\nERROR: Failed to fix Google Drive permissions!")

if __name__ == "__main__":
    main()
