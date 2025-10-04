# 🚀 Deploy to Railway (Free - No Credit Card Required)

## Prerequisites
- GitHub account
- Railway account (sign up at [railway.app](https://railway.app))

## Step 1: Prepare Your Code

1. **Push your code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/ciffox-catalog.git
   git push -u origin main
   ```

## Step 2: Deploy to Railway

1. **Go to [Railway.app](https://railway.app) and sign up**

2. **Create New Project:**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your `ciffox-catalog` repository
   - Select the `backend` folder as the root directory

3. **Set Environment Variables:**
   - Go to your project dashboard
   - Click on "Variables" tab
   - Add these variables:
     ```
     ADMIN_PASSWORD=your_secure_password
     JWT_SECRET_KEY=your-secret-key-here
     DATABASE_URL=sqlite:///./catalog.db
     GOOGLE_DRIVE_FOLDER_ID=your_folder_id
     GOOGLE_CREDENTIALS_FILE=credentials.json
     ```

4. **Deploy:**
   - Railway will automatically detect it's a Python app
   - It will install dependencies from `requirements.txt`
   - The app will start using the `Procfile`

## Step 3: Setup Google Drive

1. **Upload credentials.json:**
   - Go to your project dashboard
   - Click on "Files" tab
   - Upload your `credentials.json` file

2. **Get Google Drive Folder ID:**
   - Run the setup script locally: `python setup_google_drive.py`
   - Copy the folder ID from the output
   - Add it to Railway environment variables

## Step 4: Access Your App

Your app will be available at:
- **Public URL**: `https://your-app-name.railway.app`
- **Admin Panel**: `https://your-app-name.railway.app/admin`

## Step 5: Custom Domain (Optional)

1. Go to your project dashboard
2. Click on "Settings" → "Domains"
3. Add your custom domain
4. Update DNS records as instructed

## Monitoring

- **Logs**: View in Railway dashboard
- **Metrics**: Available in the dashboard
- **Uptime**: 99.9% guaranteed

## Cost

- **Free Tier**: $5 credit monthly (enough for small apps)
- **No Credit Card**: Required for signup
- **Upgrade**: Only if you need more resources
