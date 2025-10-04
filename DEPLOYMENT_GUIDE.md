# 🚀 Complete Deployment Guide for Ciffox Catalog

This guide will walk you through deploying your fully functional product catalog with Google Drive integration to Fly.io.

## 📋 Prerequisites

Before starting, ensure you have:

1. **Fly.io Account**: Sign up at [fly.io](https://fly.io/)
2. **Google Cloud Account**: For Google Drive API access
3. **Python 3.11+**: Installed on your local machine
4. **Git**: For version control

## 🔧 Step 1: Setup Google Drive API

### 1.1 Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.developers.google.com/)
2. Click "Create Project" or select existing project
3. Name your project (e.g., "Ciffox Catalog")
4. Click "Create"

### 1.2 Enable Google Drive API

1. In your project, go to "APIs & Services" → "Library"
2. Search for "Google Drive API"
3. Click on it and press "Enable"

### 1.3 Create OAuth 2.0 Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth 2.0 Client IDs"
3. Choose "Desktop application"
4. Name it "Ciffox Catalog Desktop"
5. Click "Create"
6. Download the JSON file and rename it to `credentials.json`
7. Place it in the `backend/` directory

### 1.4 Run Google Drive Setup

```bash
cd backend
python setup_google_drive.py
```

This will:
- Authenticate with Google Drive
- Create a dedicated folder for your catalog
- Generate configuration files
- Set up proper permissions

## 🚀 Step 2: Deploy to Fly.io

### 2.1 Install Fly.io CLI

**Windows (PowerShell):**
```powershell
iwr https://fly.io/install.ps1 -useb | iex
```

**macOS/Linux:**
```bash
curl -L https://fly.io/install.sh | sh
```

### 2.2 Login to Fly.io

```bash
flyctl auth login
```

### 2.3 Deploy Your Application

```bash
cd backend
chmod +x deploy.sh
./deploy.sh
```

### 2.4 Set Google Drive Folder ID

After deployment, set your Google Drive folder ID:

```bash
flyctl secrets set GOOGLE_DRIVE_FOLDER_ID='your_folder_id_here' --app ciffox-catalog
```

## 🔐 Step 3: Configure Security

### 3.1 Change Admin Password

```bash
flyctl secrets set ADMIN_PASSWORD='your_secure_password' --app ciffox-catalog
```

### 3.2 Set JWT Secret

```bash
flyctl secrets set JWT_SECRET_KEY='$(openssl rand -hex 32)' --app ciffox-catalog
```

## 📱 Step 4: Access Your Application

### 4.1 Public Catalog
- **URL**: `https://ciffox-catalog.fly.dev`
- **Features**: Browse products, search, responsive design

### 4.2 Admin Panel
- **URL**: `https://ciffox-catalog.fly.dev/admin`
- **Login**: Use your admin password
- **Features**: Add, edit, delete products, upload images

## 🖼️ Step 5: Upload Product Images

### 5.1 Manual Upload
1. Go to your Google Drive folder
2. Upload all product images
3. Make sure images are publicly accessible
4. Copy the image URLs

### 5.2 Update Database (Optional)
If you have existing product data, you can migrate it:

```bash
cd backend
python migrate_existing_data.py
```

## 🔍 Step 6: Verify Deployment

### 6.1 Check Application Status
```bash
flyctl status --app ciffox-catalog
```

### 6.2 View Logs
```bash
flyctl logs --app ciffox-catalog
```

### 6.3 Test Features
1. Visit the public catalog
2. Test search functionality
3. Login to admin panel
4. Add a test product
5. Verify image upload works

## 🛠️ Step 7: Customization

### 7.1 Update App Name
Edit `fly.toml`:
```toml
app = "your-app-name"
```

### 7.2 Change Region
Edit `fly.toml`:
```toml
primary_region = "lax"  # or your preferred region
```

### 7.3 Scale Resources
Edit `fly.toml`:
```toml
[[vm]]
  cpu_kind = "shared"
  cpus = 2
  memory_mb = 2048
```

## 📊 Step 8: Monitoring

### 8.1 View Metrics
```bash
flyctl metrics --app ciffox-catalog
```

### 8.2 Monitor Logs
```bash
flyctl logs --app ciffox-catalog --follow
```

### 8.3 Check Secrets
```bash
flyctl secrets list --app ciffox-catalog
```

## 🔄 Step 9: Updates and Maintenance

### 9.1 Deploy Updates
```bash
flyctl deploy --app ciffox-catalog
```

### 9.2 Restart Application
```bash
flyctl restart --app ciffox-catalog
```

### 9.3 Scale Application
```bash
flyctl scale count 2 --app ciffox-catalog
```

## 🚨 Troubleshooting

### Common Issues

#### 1. Google Drive Authentication Failed
```bash
# Check if credentials.json exists
ls -la backend/credentials.json

# Re-run setup
python setup_google_drive.py
```

#### 2. Application Won't Start
```bash
# Check logs
flyctl logs --app ciffox-catalog

# Check secrets
flyctl secrets list --app ciffox-catalog
```

#### 3. Images Not Loading
- Verify Google Drive folder is public
- Check image URLs in database
- Ensure images are in correct format (JPEG/PNG)

#### 4. Database Issues
```bash
# Connect to database
flyctl ssh console --app ciffox-catalog
sqlite3 catalog.db
```

### Getting Help

1. **Fly.io Documentation**: [fly.io/docs](https://fly.io/docs/)
2. **Google Drive API**: [developers.google.com/drive](https://developers.google.com/drive)
3. **FastAPI Documentation**: [fastapi.tiangolo.com](https://fastapi.tiangolo.com/)

## 🎉 Success!

Your Ciffox Catalog is now live and accessible worldwide! 

- **Public URL**: `https://ciffox-catalog.fly.dev`
- **Admin URL**: `https://ciffox-catalog.fly.dev/admin`
- **Google Drive Folder**: Check your Google Drive for the catalog folder

## 📈 Next Steps

1. **Customize Design**: Update CSS in `static/index.html` and `static/admin.html`
2. **Add Features**: Implement additional functionality as needed
3. **Monitor Usage**: Use Fly.io metrics to track performance
4. **Backup Data**: Regularly backup your database
5. **Scale**: Add more resources as your catalog grows

## 🔒 Security Best Practices

1. **Change Default Passwords**: Use strong, unique passwords
2. **Rotate Secrets**: Regularly update JWT secrets
3. **Monitor Access**: Check logs for suspicious activity
4. **Update Dependencies**: Keep all packages up to date
5. **Use HTTPS**: Always use secure connections

---

**Need Help?** Check the troubleshooting section or refer to the documentation links above.
