#!/usr/bin/env python3
"""Debug script to test login functionality"""

import os
import sys
import requests
import json
from datetime import datetime, timedelta
from jose import jwt

# Add backend to path
sys.path.append('backend')

def test_login_debug():
    print("=== Login Debug Test ===")
    
    # Test 1: Check environment variables
    print(f"1. ADMIN_PASSWORD env var: {repr(os.getenv('ADMIN_PASSWORD', 'NOT_SET'))}")
    print(f"2. JWT_SECRET_KEY env var: {repr(os.getenv('JWT_SECRET_KEY', 'NOT_SET'))}")
    
    # Test 2: Test server connectivity
    try:
        response = requests.get('http://localhost:8000/', timeout=5)
        print(f"3. Server connectivity: {response.status_code}")
    except Exception as e:
        print(f"3. Server connectivity ERROR: {e}")
        return
    
    # Test 3: Test login endpoint with detailed error info
    print("\n4. Testing login endpoint...")
    try:
        login_data = {"password": "admin123"}
        response = requests.post(
            'http://localhost:8000/api/login', 
            json=login_data,
            timeout=10,
            headers={'Content-Type': 'application/json'}
        )
        print(f"   Status Code: {response.status_code}")
        print(f"   Response Headers: {dict(response.headers)}")
        print(f"   Response Text: {response.text}")
        
        if response.status_code == 200:
            token_data = response.json()
            print(f"   Token: {token_data.get('access_token', 'NO_TOKEN')[:50]}...")
            
            # Test 4: Verify the token
            try:
                from main import SECRET_KEY, ALGORITHM
                payload = jwt.decode(token_data['access_token'], SECRET_KEY, algorithms=[ALGORITHM])
                print(f"   Token payload: {payload}")
            except Exception as e:
                print(f"   Token verification error: {e}")
                
    except Exception as e:
        print(f"   Login request ERROR: {e}")
    
    # Test 5: Test with different password
    print("\n5. Testing with wrong password...")
    try:
        login_data = {"password": "wrongpassword"}
        response = requests.post(
            'http://localhost:8000/api/login', 
            json=login_data,
            timeout=10
        )
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   Wrong password test ERROR: {e}")

if __name__ == "__main__":
    test_login_debug()
