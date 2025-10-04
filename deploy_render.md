# 🚀 Deploy to Render (Free - No Credit Card Required)

## Prerequisites
- GitHub account
- Render account (sign up at [render.com](https://render.com))

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

## Step 2: Deploy to Render

1. **Go to [Render.com](https://render.com) and sign up**

2. **Create New Web Service:**
   - Click "New" → "Web Service"
   - Connect your GitHub account
   - Select your `ciffox-catalog` repository
   - Choose the `backend` folder as the root directory

3. **Configure Service:**
   - **Name**: `ciffox-catalog`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

4. **Set Environment Variables:**
   - Click on "Environment" tab
   - Add these variables:
     ```
     ADMIN_PASSWORD=your_secure_password
     JWT_SECRET_KEY=your-secret-key-here
     DATABASE_URL=sqlite:///./catalog.db
     GOOGLE_DRIVE_FOLDER_ID=your_folder_id
     GOOGLE_CREDENTIALS_FILE=credentials.json
     ```

5. **Deploy:**
   - Click "Create Web Service"
   - Render will automatically build and deploy your app

## Step 3: Setup Google Drive

1. **Upload credentials.json:**
   - Go to your service dashboard
   - Click on "Files" tab
   - Upload your `credentials.json` file

2. **Get Google Drive Folder ID:**
   - Run the setup script locally: `python setup_google_drive.py`
   - Copy the folder ID from the output
   - Add it to Render environment variables

## Step 4: Access Your App

Your app will be available at:
- **Public URL**: `https://ciffox-catalog.onrender.com`
- **Admin Panel**: `https://ciffox-catalog.onrender.com/admin`

## Step 5: Custom Domain (Optional)

1. Go to your service dashboard
2. Click on "Settings" → "Custom Domains"
3. Add your custom domain
4. Update DNS records as instructed

## Monitoring

- **Logs**: View in Render dashboard
- **Metrics**: Available in the dashboard
- **Uptime**: 99.9% guaranteed

## Cost

- **Free Tier**: 750 hours/month (enough for small apps)
- **No Credit Card**: Not required
- **Upgrade**: Only if you need more resources or uptime

## Important Notes

- **Free Tier Limitations**: App sleeps after 15 minutes of inactivity
- **Cold Start**: First request after sleep may take 30-60 seconds
- **Storage**: Persistent storage available
- **SSL**: Automatic HTTPS included
