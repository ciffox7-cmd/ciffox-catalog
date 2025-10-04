from fastapi import FastAPI, HTTPException, Depends, status, File, UploadFile, Form
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from typing import List, Optional
import os
import json
import base64
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import aiofiles
from PIL import Image
import io
import httpx

# Initialize FastAPI
app = FastAPI(title="Product Catalog API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

# Database
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./catalog.db")
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Models
class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    article = Column(String, index=True)
    colour = Column(String)
    size = Column(String)
    pair = Column(String)
    price = Column(String)
    image_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Create tables
Base.metadata.create_all(bind=engine)

# Pydantic models
class ProductCreate(BaseModel):
    article: str
    colour: str
    size: str
    pair: str
    price: Optional[str] = None

class ProductUpdate(BaseModel):
    article: Optional[str] = None
    colour: Optional[str] = None
    size: Optional[str] = None
    pair: Optional[str] = None
    price: Optional[str] = None

class ProductResponse(BaseModel):
    id: int
    article: str
    colour: str
    size: str
    pair: str
    price: Optional[str] = None
    image_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class LoginRequest(BaseModel):
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# Google Drive service
class GoogleDriveService:
    def __init__(self):
        self.service = None
        self.folder_id = os.getenv("GOOGLE_DRIVE_FOLDER_ID")
        self.credentials_file = os.getenv("GOOGLE_CREDENTIALS_FILE", "credentials.json")
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Google Drive API"""
        SCOPES = ['https://www.googleapis.com/auth/drive.file']
        creds = None
        
        # Load existing credentials
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
        # If there are no valid credentials, get new ones
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if os.path.exists(self.credentials_file):
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_file, SCOPES)
                    creds = flow.run_local_server(port=0)
                else:
                    raise Exception("Google Drive credentials not found")
            
            # Save credentials for next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        
        self.service = build('drive', 'v3', credentials=creds)
    
    async def upload_image(self, file: UploadFile, product_id: int) -> str:
        """Upload image to Google Drive and return the URL"""
        try:
            # Read and process image
            contents = await file.read()
            image = Image.open(io.BytesIO(contents))
            
            # Resize if too large
            if image.width > 1920 or image.height > 1920:
                image.thumbnail((1920, 1920), Image.Resampling.LANCZOS)
            
            # Save processed image
            output = io.BytesIO()
            image.save(output, format='JPEG', quality=85)
            output.seek(0)
            
            # Upload to Google Drive
            file_metadata = {
                'name': f'product_{product_id}_{file.filename}',
                'parents': [self.folder_id] if self.folder_id else []
            }
            
            media = MediaFileUpload(
                io.BytesIO(output.getvalue()),
                mimetype='image/jpeg',
                resumable=True
            )
            
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id,webViewLink'
            ).execute()
            
            # Make file publicly viewable
            self.service.permissions().create(
                fileId=file.get('id'),
                body={'role': 'reader', 'type': 'anyone'}
            ).execute()
            
            return file.get('webViewLink')
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to upload image: {str(e)}")

# Initialize Google Drive service
try:
    drive_service = GoogleDriveService()
except Exception as e:
    print(f"Warning: Google Drive service not available: {e}")
    drive_service = None

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Authentication functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        password: str = payload.get("sub")
        if password is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return password

# Routes
@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main catalog page"""
    return FileResponse("static/index.html")

@app.get("/admin", response_class=HTMLResponse)
async def admin_page():
    """Serve the admin page"""
    return FileResponse("static/admin.html")

@app.post("/api/login", response_model=Token)
async def login(login_data: LoginRequest):
    """Admin login"""
    admin_password = os.getenv("ADMIN_PASSWORD", "admin123")
    
    # Simple password check for now (bypass bcrypt issues)
    if login_data.password != admin_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password"
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": login_data.password}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/products", response_model=List[ProductResponse])
async def get_products(db: Session = Depends(get_db)):
    """Get all products"""
    products = db.query(Product).all()
    return products

@app.post("/api/products", response_model=ProductResponse)
async def create_product(
    article: str = Form(...),
    colour: str = Form(...),
    size: str = Form(...),
    pair: str = Form(...),
    price: str = Form(None),
    image: UploadFile = File(None),
    db: Session = Depends(get_db),
    token: str = Depends(verify_token)
):
    """Create a new product (admin only)"""
    # Create product first
    db_product = Product(
        article=article,
        colour=colour,
        size=size,
        pair=pair,
        price=price
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    
    # Upload image if provided
    if image and drive_service:
        try:
            image_url = await drive_service.upload_image(image, db_product.id)
            db_product.image_url = image_url
            db.commit()
            db.refresh(db_product)
        except Exception as e:
            print(f"Image upload failed: {e}")
    
    return db_product

@app.put("/api/products/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    product_update: ProductUpdate,
    db: Session = Depends(get_db),
    token: str = Depends(verify_token)
):
    """Update a product (admin only)"""
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    update_data = product_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_product, field, value)
    
    db_product.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_product)
    return db_product

@app.delete("/api/products/{product_id}")
async def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    token: str = Depends(verify_token)
):
    """Delete a product (admin only)"""
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted successfully"}

@app.post("/api/products/{product_id}/image")
async def upload_product_image(
    product_id: int,
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
    token: str = Depends(verify_token)
):
    """Upload image for a product (admin only)"""
    if not drive_service:
        raise HTTPException(status_code=500, detail="Google Drive service not available")
    
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    try:
        image_url = await drive_service.upload_image(image, product_id)
        db_product.image_url = image_url
        db.commit()
        db.refresh(db_product)
        return {"image_url": image_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload image: {str(e)}")


@app.get("/api/proxy-image")
async def proxy_image(url: str):
    """Proxy Google Drive images to bypass CORS restrictions"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=30.0)
            if response.status_code == 200:
                return StreamingResponse(
                    io.BytesIO(response.content),
                    media_type=response.headers.get("content-type", "image/jpeg"),
                    headers={
                        "Cache-Control": "public, max-age=3600",
                        "Access-Control-Allow-Origin": "*"
                    }
                )
            else:
                raise HTTPException(status_code=response.status_code, detail="Failed to fetch image")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Proxy error: {str(e)}")


# Mount static files
import os
static_dir = "static"
if not os.path.exists(static_dir):
    os.makedirs(static_dir)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
