#!/usr/bin/env python3
"""
Quick setup script for free hosting deployment
"""

import os
import json
import subprocess
import sys

def setup_free_hosting():
    """Setup the application for free hosting deployment"""
    print("[SETUP] Setting up Ciffox Catalog for Free Hosting")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("backend/main.py"):
        print("[ERROR] Please run this script from the project root directory")
        return False
    
    print("[OK] Found backend application")
    
    # Create .env file for local development
    env_content = """# Local development environment variables
ADMIN_PASSWORD=admin123
JWT_SECRET_KEY=your-secret-key-change-this-in-production
DATABASE_URL=sqlite:///./catalog.db
GOOGLE_DRIVE_FOLDER_ID=your_folder_id_here
GOOGLE_CREDENTIALS_FILE=credentials.json
"""
    
    with open("backend/.env", "w") as f:
        f.write(env_content)
    
    print("[OK] Created .env file for local development")
    
    # Check if Google Drive setup is needed
    if not os.path.exists("backend/credentials.json"):
        print("\n[INFO] Google Drive Setup Required:")
        print("1. Go to https://console.developers.google.com/")
        print("2. Create a new project")
        print("3. Enable Google Drive API")
        print("4. Create OAuth 2.0 credentials (Desktop application)")
        print("5. Download credentials.json to backend/ directory")
        print("6. Run: python backend/setup_google_drive.py")
    else:
        print("[OK] Google Drive credentials found")
    
    # Create deployment instructions
    instructions = """
# Your Ciffox Catalog is Ready for Free Hosting!

## Choose Your Hosting Platform:

### Option 1: Railway (Recommended)
- Free tier: $5 credit monthly
- No credit card required
- Easy deployment from GitHub
- Global CDN included

**Steps:**
1. Push code to GitHub
2. Sign up at railway.app
3. Deploy from GitHub repo
4. Set environment variables
5. Upload credentials.json

### Option 2: Render
- Free tier: 750 hours/month
- No credit card required
- Automatic deployments
- SSL included

**Steps:**
1. Push code to GitHub
2. Sign up at render.com
3. Create web service
4. Set environment variables
5. Upload credentials.json

## Quick Start:

1. **Setup Google Drive:**
   ```bash
   cd backend
   python setup_google_drive.py
   ```

2. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/ciffox-catalog.git
   git push -u origin main
   ```

3. **Deploy to Railway or Render:**
   - Follow the deployment guides in deploy_railway.md or deploy_render.md

## Your App Will Be Available At:
- Public Catalog: https://your-app-name.railway.app (or .onrender.com)
- Admin Panel: https://your-app-name.railway.app/admin
- Default Password: admin123 (change this!)

## Need Help?
- Check deploy_railway.md for Railway deployment
- Check deploy_render.md for Render deployment
- Both platforms have excellent documentation
"""
    
    with open("DEPLOYMENT_INSTRUCTIONS.md", "w") as f:
        f.write(instructions)
    
    print("[OK] Created deployment instructions")
    
    print("\n[SUCCESS] Setup Complete!")
    print("[NEXT] Next steps:")
    print("1. Setup Google Drive API (if not done)")
    print("2. Push code to GitHub")
    print("3. Deploy to Railway or Render")
    print("4. Access your live catalog!")
    
    return True

if __name__ == "__main__":
    success = setup_free_hosting()
    if not success:
        sys.exit(1)
