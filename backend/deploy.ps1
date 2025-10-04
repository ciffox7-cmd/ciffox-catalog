# Ciffox Catalog Deployment Script for Fly.io (Windows PowerShell)
Write-Host "🚀 Deploying Ciffox Catalog to Fly.io" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green

# Check if flyctl is installed
try {
    $flyctlVersion = flyctl version 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "flyctl not found"
    }
    Write-Host "✅ flyctl found" -ForegroundColor Green
} catch {
    Write-Host "❌ flyctl is not installed!" -ForegroundColor Red
    Write-Host "📋 Please install flyctl first:" -ForegroundColor Yellow
    Write-Host "   Run: iwr https://fly.io/install.ps1 -useb | iex" -ForegroundColor Yellow
    exit 1
}

# Check if user is logged in
try {
    $whoami = flyctl auth whoami 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "Not logged in"
    }
    Write-Host "✅ Logged in to Fly.io as: $whoami" -ForegroundColor Green
} catch {
    Write-Host "🔐 Please log in to Fly.io first:" -ForegroundColor Yellow
    flyctl auth login
}

# Check if app exists
$appExists = flyctl apps list 2>$null | Select-String "ciffox-catalog"
if ($appExists) {
    Write-Host "✅ App 'ciffox-catalog' exists" -ForegroundColor Green
} else {
    Write-Host "📱 Creating new app 'ciffox-catalog'..." -ForegroundColor Yellow
    flyctl apps create ciffox-catalog --generate-name=false
}

# Set environment variables
Write-Host "🔧 Setting environment variables..." -ForegroundColor Yellow
flyctl secrets set ADMIN_PASSWORD="admin123" --app ciffox-catalog
flyctl secrets set JWT_SECRET_KEY="$(openssl rand -hex 32)" --app ciffox-catalog

# Check if Google Drive folder ID is set
$env:GOOGLE_DRIVE_FOLDER_ID = $env:GOOGLE_DRIVE_FOLDER_ID
if ([string]::IsNullOrEmpty($env:GOOGLE_DRIVE_FOLDER_ID)) {
    Write-Host "⚠️  GOOGLE_DRIVE_FOLDER_ID not set!" -ForegroundColor Yellow
    Write-Host "📋 Please run: python setup_google_drive.py first" -ForegroundColor Yellow
    Write-Host "   Then set the folder ID:" -ForegroundColor Yellow
    Write-Host "   flyctl secrets set GOOGLE_DRIVE_FOLDER_ID='your_folder_id' --app ciffox-catalog" -ForegroundColor Yellow
}

# Deploy the application
Write-Host "🚀 Deploying application..." -ForegroundColor Yellow
flyctl deploy --app ciffox-catalog

Write-Host "✅ Deployment complete!" -ForegroundColor Green
Write-Host "🌐 Your app should be available at: https://ciffox-catalog.fly.dev" -ForegroundColor Cyan
Write-Host "🔧 Admin panel: https://ciffox-catalog.fly.dev/admin" -ForegroundColor Cyan
Write-Host "🔑 Default admin password: admin123" -ForegroundColor Cyan
Write-Host ""
Write-Host "📋 Don't forget to:" -ForegroundColor Yellow
Write-Host "1. Change the admin password in production" -ForegroundColor Yellow
Write-Host "2. Set up Google Drive folder ID if not done already" -ForegroundColor Yellow
Write-Host "3. Upload your product images to Google Drive" -ForegroundColor Yellow
