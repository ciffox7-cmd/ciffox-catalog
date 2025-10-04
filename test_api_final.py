import requests

# Test API endpoint
url = "http://localhost:8000/api/products"

print(f"Testing API endpoint: {url}")
try:
    response = requests.get(url)
    print(f"Status Code: {response.status_code}")
    print(f"Headers: {response.headers}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Success! Found {len(data)} products")
        if data:
            print(f"Sample product:")
            print(f"  ID: {data[0]['id']}")
            print(f"  Article: {data[0]['article']}")
            print(f"  Colour: {data[0]['colour']}")
            print(f"  Size: {data[0]['size']}")
            print(f"  Pair: {data[0]['pair']}")
            print(f"  Price: {data[0]['price']}")
            print(f"  Image URL: {data[0]['image_url']}")
            print(f"  Created At: {data[0]['created_at']}")
            print(f"  Updated At: {data[0]['updated_at']}")
    else:
        print(f"Error: {response.text}")
        
except Exception as e:
    print(f"Error: {e}")

