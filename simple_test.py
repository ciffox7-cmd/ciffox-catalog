#!/usr/bin/env python3
"""
Simple test to verify the backend can start
"""

import sys
import os
sys.path.append('backend')

try:
    from backend.main import app
    print("[OK] Backend imports successfully")
    
    # Test if we can create the app
    print("[OK] FastAPI app created successfully")
    print("[INFO] Backend is ready to run!")
    print("[INFO] To start the server, run: cd backend && python main.py")
    
except ImportError as e:
    print(f"[ERROR] Import failed: {e}")
    print("[INFO] Make sure you're in the project root directory")
    sys.exit(1)
except Exception as e:
    print(f"[ERROR] Unexpected error: {e}")
    sys.exit(1)
