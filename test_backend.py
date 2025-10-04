#!/usr/bin/env python3
"""
Test script to verify the backend is working correctly
"""

import requests
import time
import json

def test_backend():
    """Test the backend endpoints"""
    base_url = "http://localhost:8000"
    
    print("[TEST] Testing Ciffox Catalog Backend")
    print("=" * 40)
    
    # Wait for server to start
    print("[WAIT] Waiting for server to start...")
    time.sleep(3)
    
    try:
        # Test 1: Health check (main page)
        print("[1] Testing main page...")
        response = requests.get(f"{base_url}/", timeout=10)
        if response.status_code == 200:
            print("[OK] Main page accessible")
        else:
            print(f"[ERROR] Main page failed: {response.status_code}")
            return False
        
        # Test 2: Admin page
        print("[2] Testing admin page...")
        response = requests.get(f"{base_url}/admin", timeout=10)
        if response.status_code == 200:
            print("[OK] Admin page accessible")
        else:
            print(f"[ERROR] Admin page failed: {response.status_code}")
            return False
        
        # Test 3: API endpoints
        print("[3] Testing API endpoints...")
        response = requests.get(f"{base_url}/api/products", timeout=10)
        if response.status_code == 200:
            products = response.json()
            print(f"[OK] Products API working - {len(products)} products found")
        else:
            print(f"[ERROR] Products API failed: {response.status_code}")
            return False
        
        # Test 4: Login endpoint
        print("[4] Testing login endpoint...")
        login_data = {"password": "admin123"}
        response = requests.post(f"{base_url}/api/login", json=login_data, timeout=10)
        if response.status_code == 200:
            token_data = response.json()
            print("[OK] Login endpoint working")
            print(f"   Token type: {token_data.get('token_type')}")
        else:
            print(f"[ERROR] Login endpoint failed: {response.status_code}")
            return False
        
        print("\n[SUCCESS] All tests passed! Backend is working correctly.")
        print(f"[URL] Main page: {base_url}")
        print(f"[URL] Admin panel: {base_url}/admin")
        print("[INFO] Default admin password: admin123")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("[ERROR] Could not connect to server. Make sure it's running on port 8000")
        return False
    except Exception as e:
        print(f"[ERROR] Test failed with error: {e}")
        return False

if __name__ == "__main__":
    success = test_backend()
    if not success:
        print("\n[TIPS] Troubleshooting tips:")
        print("1. Make sure the server is running: python main.py")
        print("2. Check if port 8000 is available")
        print("3. Verify all dependencies are installed")
        exit(1)
