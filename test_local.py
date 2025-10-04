#!/usr/bin/env python3
"""
Simple local test for the Ciffox Catalog backend
"""

import sys
import os
sys.path.append('backend')

def test_imports():
    """Test if all required modules can be imported"""
    print("[TEST] Testing imports...")
    
    try:
        import fastapi
        print("[OK] FastAPI imported")
    except ImportError as e:
        print(f"[ERROR] FastAPI import failed: {e}")
        return False
    
    try:
        import uvicorn
        print("[OK] Uvicorn imported")
    except ImportError as e:
        print(f"[ERROR] Uvicorn import failed: {e}")
        return False
    
    try:
        import sqlalchemy
        print("[OK] SQLAlchemy imported")
    except ImportError as e:
        print(f"[ERROR] SQLAlchemy import failed: {e}")
        return False
    
    try:
        from backend.main import app
        print("[OK] Main app imported")
    except ImportError as e:
        print(f"[ERROR] Main app import failed: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Main app error: {e}")
        return False
    
    return True

def test_simple_server():
    """Test running a simple server"""
    print("\n[TEST] Testing simple server...")
    
    try:
        import uvicorn
        from backend.main import app
        
        print("[INFO] Starting server on http://localhost:8000")
        print("[INFO] Press Ctrl+C to stop")
        print("[INFO] Open http://localhost:8000 in your browser")
        
        uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
        
    except Exception as e:
        print(f"[ERROR] Server failed: {e}")
        return False

if __name__ == "__main__":
    print("[TEST] Ciffox Catalog Local Test")
    print("=" * 40)
    
    if test_imports():
        print("\n[SUCCESS] All imports working!")
        print("\n[INFO] Starting local server...")
        test_simple_server()
    else:
        print("\n[ERROR] Import tests failed!")
        print("[INFO] Install missing dependencies:")
        print("cd backend && pip install -r requirements.txt")
        sys.exit(1)
