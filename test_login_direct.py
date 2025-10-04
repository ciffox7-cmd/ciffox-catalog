#!/usr/bin/env python3
"""Direct test of login function"""

import os
import sys
from datetime import datetime, timedelta

# Add backend to path
sys.path.insert(0, 'backend')

def test_login_direct():
    print("=== Direct Login Function Test ===")
    
    try:
        # Import the login function and related components
        from main import login, LoginRequest, create_access_token, SECRET_KEY, ALGORITHM
        from jose import jwt
        
        print(f"1. SECRET_KEY: {SECRET_KEY}")
        print(f"2. ALGORITHM: {ALGORITHM}")
        print(f"3. ADMIN_PASSWORD env: {os.getenv('ADMIN_PASSWORD', 'NOT_SET')}")
        
        # Test the password check logic
        admin_password = os.getenv("ADMIN_PASSWORD", "admin123")
        print(f"4. Expected password: {repr(admin_password)}")
        
        # Test password comparison
        test_password = "admin123"
        print(f"5. Test password: {repr(test_password)}")
        print(f"6. Password match: {test_password == admin_password}")
        
        # Test JWT creation
        try:
            access_token_expires = timedelta(minutes=15)
            access_token = create_access_token(
                data={"sub": test_password}, 
                expires_delta=access_token_expires
            )
            print(f"7. JWT created successfully: {access_token[:50]}...")
            
            # Test JWT decoding
            payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
            print(f"8. JWT decoded successfully: {payload}")
            
        except Exception as e:
            print(f"7. JWT creation/decoding error: {e}")
            import traceback
            traceback.print_exc()
            
    except Exception as e:
        print(f"Import or function error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_login_direct()
