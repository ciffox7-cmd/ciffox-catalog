import requests

# Test the backend after fixing static file path
print("Testing backend after fixes...")

# Test the root endpoint
try:
    response = requests.get("http://localhost:8000/")
    print(f"Root endpoint status: {response.status_code}")
    if response.status_code == 200:
        print("OK Root endpoint working!")
    else:
        print(f"X Root endpoint error: {response.text[:200]}")
except Exception as e:
    print(f"X Root endpoint error: {e}")

# Test the API endpoint
try:
    response = requests.get("http://localhost:8000/api/products")
    print(f"API endpoint status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"OK API endpoint working! Found {len(data)} products")
    else:
        print(f"X API endpoint error: {response.text[:200]}")
except Exception as e:
    print(f"X API endpoint error: {e}")

# Test the admin endpoint
try:
    response = requests.get("http://localhost:8000/admin")
    print(f"Admin endpoint status: {response.status_code}")
    if response.status_code == 200:
        print("OK Admin endpoint working!")
    else:
        print(f"X Admin endpoint error: {response.text[:200]}")
except Exception as e:
    print(f"X Admin endpoint error: {e}")
