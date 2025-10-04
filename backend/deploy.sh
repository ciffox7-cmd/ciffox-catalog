#!/bin/bash

# Ciffox Catalog Deployment Script for Fly.io
echo "🚀 Deploying Ciffox Catalog to Fly.io"
echo "======================================"

# Check if flyctl is installed
if ! command -v flyctl &> /dev/null; then
    echo "❌ flyctl is not installed!"
    echo "📋 Please install flyctl first:"
    echo "   Windows: iwr https://fly.io/install.ps1 -useb | iex"
    echo "   macOS: curl -L https://fly.io/install.sh | sh"
    echo "   Linux: curl -L https://fly.io/install.sh | sh"
    exit 1
fi

echo "✅ flyctl found"

# Check if user is logged in
if ! flyctl auth whoami &> /dev/null; then
    echo "🔐 Please log in to Fly.io first:"
    flyctl auth login
fi

echo "✅ Logged in to Fly.io"

# Check if app exists
if flyctl apps list | grep -q "ciffox-catalog"; then
    echo "✅ App 'ciffox-catalog' exists"
else
    echo "📱 Creating new app 'ciffox-catalog'..."
    flyctl apps create ciffox-catalog --generate-name=false
fi

# Set environment variables
echo "🔧 Setting environment variables..."
flyctl secrets set ADMIN_PASSWORD="admin123" --app ciffox-catalog
flyctl secrets set JWT_SECRET_KEY="$(openssl rand -hex 32)" --app ciffox-catalog

# Check if Google Drive folder ID is set
if [ -z "$GOOGLE_DRIVE_FOLDER_ID" ]; then
    echo "⚠️  GOOGLE_DRIVE_FOLDER_ID not set!"
    echo "📋 Please run: python setup_google_drive.py first"
    echo "   Then set the folder ID:"
    echo "   flyctl secrets set GOOGLE_DRIVE_FOLDER_ID='your_folder_id' --app ciffox-catalog"
fi

# Deploy the application
echo "🚀 Deploying application..."
flyctl deploy --app ciffox-catalog

echo "✅ Deployment complete!"
echo "🌐 Your app should be available at: https://ciffox-catalog.fly.dev"
echo "🔧 Admin panel: https://ciffox-catalog.fly.dev/admin"
echo "🔑 Default admin password: admin123"
echo ""
echo "📋 Don't forget to:"
echo "1. Change the admin password in production"
echo "2. Set up Google Drive folder ID if not done already"
echo "3. Upload your product images to Google Drive"
