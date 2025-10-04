
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
