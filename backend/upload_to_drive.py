#!/usr/bin/env python3
"""
Script to upload product images to Google Drive and update database URLs
"""

import os
import sqlite3
import json
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

# Scopes required for the application
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def upload_images_to_drive():
    """Upload product images to Google Drive and update database"""
    print("Uploading product images to Google Drive...")
    
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
        cursor.execute("SELECT id, article, image_url FROM products ORDER BY id")
        products = cursor.fetchall()
        
        print(f"Found {len(products)} products to process")
        
        # Get available images
        thumbs_dir = Path("../output/thumbs")
        available_images = list(thumbs_dir.glob("*.jpg"))
        
        uploaded_count = 0
        updated_count = 0
        
        for i, (product_id, article, current_url) in enumerate(products):
            if i < len(available_images):
                image_path = available_images[i]
                image_name = image_path.name
                
                print(f"Processing product {product_id} ({article}) with image {image_name}")
                
                try:
                    # Upload image to Google Drive
                    file_metadata = {
                        'name': f'product_{product_id}_{image_name}',
                        'parents': [folder_id]
                    }
                    
                    media = MediaFileUpload(
                        str(image_path),
                        mimetype='image/jpeg',
                        resumable=True
                    )
                    
                    file = service.files().create(
                        body=file_metadata,
                        media_body=media,
                        fields='id,webViewLink'
                    ).execute()
                    
                    # Make file publicly viewable
                    service.permissions().create(
                        fileId=file.get('id'),
                        body={'role': 'reader', 'type': 'anyone'}
                    ).execute()
                    
                    # Get the direct image URL
                    image_url = f"https://drive.google.com/uc?id={file.get('id')}"
                    
                    # Update database
                    cursor.execute("""
                        UPDATE products 
                        SET image_url = ? 
                        WHERE id = ?
                    """, (image_url, product_id))
                    
                    uploaded_count += 1
                    updated_count += 1
                    print(f"SUCCESS: Uploaded and updated product {product_id}")
                    
                except HttpError as e:
                    print(f"ERROR: Failed to upload image for product {product_id}: {e}")
                    continue
                except Exception as e:
                    print(f"ERROR: Unexpected error for product {product_id}: {e}")
                    continue
            else:
                print(f"WARNING: No image available for product {product_id} ({article})")
        
        conn.commit()
        conn.close()
        
        print(f"\nUpload Summary:")
        print(f"Images uploaded: {uploaded_count}")
        print(f"Database records updated: {updated_count}")
        print(f"Total products processed: {len(products)}")
        
        return True
        
    except Exception as e:
        print(f"ERROR: Failed to create Google Drive service: {e}")
        return False

def main():
    """Main function"""
    print("Ciffox Catalog - Upload Images to Google Drive")
    print("=" * 50)
    
    if upload_images_to_drive():
        print("\nSUCCESS: Image upload completed!")
        print("\nNext steps:")
        print("1. Restart your application server")
        print("2. Check the catalog to see images from Google Drive")
        print("3. Verify images are loading correctly")
    else:
        print("\nERROR: Image upload failed!")

if __name__ == "__main__":
    main()
