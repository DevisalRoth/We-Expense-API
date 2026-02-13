import requests
from jose import jwt
import time

# Configuration
BASE_URL = "http://localhost:8002"

def verify_protection():
    print("Verifying protection of previously unprotected endpoints...")
    
    # 1. Try to access friends without token
    print("\n1. Accessing /friends/ without token (should fail)...")
    try:
        response = requests.get(f"{BASE_URL}/friends/")
        if response.status_code == 401:
            print("✅ SUCCESS: /friends/ is protected (401 Unauthorized)")
        else:
            print(f"❌ FAILED: /friends/ returned {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

    # 2. Try to access saved-items without token
    print("\n2. Accessing /saved-items/ without token (should fail)...")
    try:
        response = requests.get(f"{BASE_URL}/saved-items/")
        if response.status_code == 401:
            print("✅ SUCCESS: /saved-items/ is protected (401 Unauthorized)")
        else:
            print(f"❌ FAILED: /saved-items/ returned {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

    # 3. Get a valid token
    email = f"test_prot_{int(time.time())}@example.com"
    password = "securepassword123"
    print(f"\n3. Registering user {email}...")
    requests.post(f"{BASE_URL}/register", json={"email": email, "password": password})
    
    login_response = requests.post(f"{BASE_URL}/token", data={"username": email, "password": password})
    if login_response.status_code != 200:
        print("Login failed, skipping authenticated tests")
        return
        
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 4. Try to access friends WITH token
    print("\n4. Accessing /friends/ WITH token (should succeed)...")
    try:
        response = requests.get(f"{BASE_URL}/friends/", headers=headers)
        if response.status_code == 200:
            print("✅ SUCCESS: /friends/ accepted token (200 OK)")
        else:
            print(f"❌ FAILED: /friends/ rejected token: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    try:
        verify_protection()
    except requests.exceptions.ConnectionError:
        print("Could not connect to server. Is it running on port 8002?")
