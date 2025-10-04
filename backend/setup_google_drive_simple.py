#!/usr/bin/env python3
"""
Google Drive API Setup Script for Ciffox Catalog
This script helps you set up Google Drive API credentials and create a folder for your catalog.
"""

import os
import json
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Scopes required for the application
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def setup_google_drive():
    """Set up Google Drive API credentials and create folder"""
    print("Setting up Google Drive API for Ciffox Catalog")
    print("=" * 50)
    
    # Check if credentials file exists
    credentials_file = 'credentials.json'
    if not os.path.exists(credentials_file):
        print("ERROR: credentials.json not found!")
        print("\nTo get credentials.json:")
        print("1. Go to https://console.developers.google.com/")
        print("2. Create a new project or select existing one")
        print("3. Enable Google Drive API")
        print("4. Go to 'Credentials' -> 'Create Credentials' -> 'OAuth 2.0 Client IDs'")
        print("5. Choose 'Desktop application'")
        print("6. Download the JSON file and rename it to 'credentials.json'")
        print("7. Place it in the backend/ directory")
        return False
    
    print("SUCCESS: credentials.json found")
    
    # Authenticate and get credentials
    creds = None
    token_file = 'token.json'
    
    # Load existing token
    if os.path.exists(token_file):
        print("SUCCESS: Loading existing token...")
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    
    # If no valid credentials, get new ones
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing expired token...")
            creds.refresh(Request())
        else:
            print("Starting OAuth flow...")
            flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save credentials for next run
        with open(token_file, 'w') as token:
            token.write(creds.to_json())
        print("SUCCESS: Token saved to token.json")
    
    # Create Drive service
    try:
        service = build('drive', 'v3', credentials=creds)
        print("SUCCESS: Google Drive service created")
        
        # Create folder for catalog
        folder_name = "Ciffox Product Catalog"
        folder_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        
        # Check if folder already exists
        results = service.files().list(
            q=f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'",
            fields="files(id, name)"
        ).execute()
        
        if results['files']:
            folder_id = results['files'][0]['id']
            print(f"SUCCESS: Folder '{folder_name}' already exists (ID: {folder_id})")
        else:
            # Create new folder
            folder = service.files().create(
                body=folder_metadata,
                fields='id'
            ).execute()
            folder_id = folder.get('id')
            print(f"SUCCESS: Created folder '{folder_name}' (ID: {folder_id})")
        
        # Make folder publicly accessible
        try:
            service.permissions().create(
                fileId=folder_id,
                body={'role': 'reader', 'type': 'anyone'}
            ).execute()
            print("SUCCESS: Folder made publicly accessible")
        except HttpError as e:
            print(f"WARNING: Could not make folder public: {e}")
        
        # Create .env file with configuration
        env_content = f"""# Admin credentials
ADMIN_PASSWORD=admin123

# Google Drive API credentials
GOOGLE_DRIVE_FOLDER_ID={folder_id}
GOOGLE_CREDENTIALS_FILE=credentials.json

# JWT secret (change this in production!)
JWT_SECRET_KEY=your-secret-key-change-this-in-production

# Database
DATABASE_URL=sqlite:///./catalog.db
"""
        
        with open('.env', 'w') as f:
            f.write(env_content)
        
        print("SUCCESS: Created .env file with configuration")
        print("\nGoogle Drive setup complete!")
        print(f"Folder ID: {folder_id}")
        print("You can view your folder at: https://drive.google.com/drive/folders/" + folder_id)
        
        return True
        
    except HttpError as e:
        print(f"ERROR: Google Drive API error: {e}")
        return False
    except Exception as e:
        print(f"ERROR: Unexpected error: {e}")
        return False

def main():
    """Main function"""
    print("Welcome to Ciffox Catalog Google Drive Setup!")
    print("This script will help you configure Google Drive API access.")
    print()
    
    if setup_google_drive():
        print("\nSUCCESS: Setup completed successfully!")
        print("\nNext steps:")
        print("1. Review the .env file and change the ADMIN_PASSWORD and JWT_SECRET_KEY")
        print("2. Deploy your application to Fly.io")
        print("3. Upload your product images to the Google Drive folder")
        print("4. Start adding products through the admin panel!")
    else:
        print("\nERROR: Setup failed. Please check the errors above and try again.")

if __name__ == "__main__":
    main()
