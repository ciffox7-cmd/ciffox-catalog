#!/usr/bin/env python3
"""
Quick test to verify the server is working
"""

import requests
import time
import sys

def test_server():
    """Test if the server is responding"""
    print("[TEST] Testing Ciffox Catalog Server")
    print("=" * 40)
    
    # Wait a moment for server to start
    print("[WAIT] Waiting for server to start...")
    time.sleep(2)
    
    try:
        # Test main page
        print("[1] Testing main page...")
        response = requests.get("http://localhost:8000/", timeout=10)
        if response.status_code == 200:
            print("[OK] Main page accessible")
        else:
            print(f"[ERROR] Main page failed: {response.status_code}")
            return False
        
        # Test admin page
        print("[2] Testing admin page...")
        response = requests.get("http://localhost:8000/admin", timeout=10)
        if response.status_code == 200:
            print("[OK] Admin page accessible")
        else:
            print(f"[ERROR] Admin page failed: {response.status_code}")
            return False
        
        # Test API
        print("[3] Testing API...")
        response = requests.get("http://localhost:8000/api/products", timeout=10)
        if response.status_code == 200:
            products = response.json()
            print(f"[OK] API working - {len(products)} products found")
        else:
            print(f"[ERROR] API failed: {response.status_code}")
            return False
        
        print("\n[SUCCESS] All tests passed!")
        print("[URL] Main page: http://localhost:8000")
        print("[URL] Admin panel: http://localhost:8000/admin")
        print("[INFO] Default admin password: admin123")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("[ERROR] Could not connect to server")
        print("[INFO] Make sure the server is running on port 8000")
        return False
    except Exception as e:
        print(f"[ERROR] Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_server()
    if not success:
        print("\n[TIPS] Troubleshooting:")
        print("1. Start the server: python test_local.py")
        print("2. Wait for it to start completely")
        print("3. Run this test in another terminal")
        sys.exit(1)
