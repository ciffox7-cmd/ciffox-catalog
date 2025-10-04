# Ciffox Product Catalog

A full-stack web application for managing and displaying product catalogs with Google Drive integration.

## Features

- **Public Catalog**: Beautiful, responsive product catalog for customers
- **Admin Panel**: Secure admin interface for managing products
- **Google Drive Integration**: Automatic image upload and storage
- **Real-time Search**: Instant product search and filtering
- **Mobile Responsive**: Works perfectly on all devices
- **Cloud Deployed**: Ready for Fly.io deployment

## Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite
- **Storage**: Google Drive API
- **Deployment**: Fly.io
- **Authentication**: JWT tokens

## Quick Start

### 1. Setup Google Drive API

```bash
# Run the setup script
python setup_google_drive.py
```

This will:
- Guide you through Google Drive API setup
- Create a dedicated folder for your catalog
- Generate configuration files

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Locally

```bash
python main.py
```

Visit `http://localhost:8000` to see your catalog!

### 4. Deploy to Fly.io

```bash
# Make deploy script executable
chmod +x deploy.sh

# Deploy to Fly.io
./deploy.sh
```

## Configuration

### Environment Variables

Create a `.env` file with:

```env
# Admin credentials
ADMIN_PASSWORD=your_secure_password

# Google Drive API
GOOGLE_DRIVE_FOLDER_ID=your_folder_id
GOOGLE_CREDENTIALS_FILE=credentials.json

# JWT secret (change in production!)
JWT_SECRET_KEY=your-secret-key-here

# Database
DATABASE_URL=sqlite:///./catalog.db
```

### Google Drive Setup

1. Go to [Google Cloud Console](https://console.developers.google.com/)
2. Create a new project
3. Enable Google Drive API
4. Create OAuth 2.0 credentials (Desktop application)
5. Download `credentials.json` to the backend directory
6. Run `python setup_google_drive.py`

## Usage

### Public Users
- Visit the main page to browse products
- Use the search bar to find specific products
- View product details, images, and prices

### Admin Users
- Go to `/admin` and login with your password
- Add new products with images
- Edit existing product information
- Delete products
- All images are automatically uploaded to Google Drive

## API Endpoints

- `GET /` - Public catalog page
- `GET /admin` - Admin panel
- `POST /api/login` - Admin authentication
- `GET /api/products` - Get all products
- `POST /api/products` - Create product (admin)
- `PUT /api/products/{id}` - Update product (admin)
- `DELETE /api/products/{id}` - Delete product (admin)
- `POST /api/products/{id}/image` - Upload product image (admin)

## Deployment on Fly.io

### Prerequisites
- [Fly.io account](https://fly.io/)
- [flyctl installed](https://fly.io/docs/hands-on/install-flyctl/)

### Deploy Steps

1. **Login to Fly.io**:
   ```bash
   flyctl auth login
   ```

2. **Setup Google Drive**:
   ```bash
   python setup_google_drive.py
   ```

3. **Deploy**:
   ```bash
   ./deploy.sh
   ```

4. **Set Google Drive Folder ID**:
   ```bash
   flyctl secrets set GOOGLE_DRIVE_FOLDER_ID='your_folder_id' --app ciffox-catalog
   ```

### Manual Deployment

```bash
# Create app
flyctl apps create ciffox-catalog

# Set secrets
flyctl secrets set ADMIN_PASSWORD="your_password" --app ciffox-catalog
flyctl secrets set JWT_SECRET_KEY="$(openssl rand -hex 32)" --app ciffox-catalog
flyctl secrets set GOOGLE_DRIVE_FOLDER_ID="your_folder_id" --app ciffox-catalog

# Deploy
flyctl deploy --app ciffox-catalog
```

## File Structure

```
backend/
├── main.py                 # FastAPI application
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration
├── fly.toml              # Fly.io configuration
├── setup_google_drive.py # Google Drive setup script
├── deploy.sh             # Deployment script
├── static/               # Frontend files
│   ├── index.html        # Public catalog page
│   ├── admin.html        # Admin panel
│   └── placeholder.jpg   # Default product image
├── credentials.json      # Google Drive API credentials
├── token.json           # Google Drive access token
└── .env                 # Environment variables
```

## Security Notes

- Change the default admin password in production
- Use a strong JWT secret key
- Keep your Google Drive credentials secure
- Consider using environment variables for sensitive data

## Troubleshooting

### Google Drive Issues
- Ensure `credentials.json` is in the backend directory
- Check that the Google Drive API is enabled
- Verify the folder ID is correct

### Deployment Issues
- Check Fly.io logs: `flyctl logs --app ciffox-catalog`
- Verify all secrets are set: `flyctl secrets list --app ciffox-catalog`
- Ensure the app is running: `flyctl status --app ciffox-catalog`

### Local Development
- Make sure all dependencies are installed
- Check that the database file is created
- Verify Google Drive authentication

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review Fly.io documentation
3. Check Google Drive API documentation
4. Open an issue in the repository

## License

This project is open source and available under the MIT License.
