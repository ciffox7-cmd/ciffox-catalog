#!/usr/bin/env python3
"""Minimal test for login functionality"""

import os
import sys
import requests
import json
from datetime import datetime, timedelta

# Add backend to path
sys.path.append('backend')

def test_minimal_login():
    print("=== Minimal Login Test ===")
    
    # Test the login endpoint with minimal data
    login_data = {"password": "admin123"}
    
    try:
        print(f"Sending login request with data: {login_data}")
        response = requests.post(
            'http://localhost:8000/api/login', 
            json=login_data,
            timeout=10,
            headers={'Content-Type': 'application/json'}
        )
        print(f"Response status: {response.status_code}")
        print(f"Response text: {response.text}")
        
        # Try to get more details about the error
        if response.status_code == 500:
            print("\nTrying to get error details...")
            try:
                error_response = requests.post(
                    'http://localhost:8000/api/login', 
                    json=login_data,
                    timeout=10,
                    headers={
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'
                    }
                )
                print(f"Error response: {error_response.text}")
            except Exception as e:
                print(f"Error getting details: {e}")
                
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_minimal_login()
