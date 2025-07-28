#!/usr/bin/env python3
"""
Test script for backend login fixes
"""

import subprocess
import sys
import time

def install_requests():
    """Install requests if not available"""
    try:
        import requests
        return True
    except ImportError:
        print("Installing requests...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
            return True
        except subprocess.CalledProcessError:
            print("Failed to install requests. Please install manually: pip install requests")
            return False

def test_api_endpoints():
    """Test API endpoints"""
    import requests
    
    BASE_URL = "https://hakon-56ae06ddc8d1.herokuapp.com"
    
    print("=== Testing Backend Fixes ===\n")
    
    # Test 1: Health check
    print("1. Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        if response.status_code == 200:
            print("   ✅ Health check passed")
        else:
            print("   ❌ Health check failed")
    except Exception as e:
        print(f"   ❌ Health check error: {e}")
    
    # Test 2: Root endpoint
    print("\n2. Testing root endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=10)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        if response.status_code == 200:
            print("   ✅ Root endpoint passed")
        else:
            print("   ❌ Root endpoint failed")
    except Exception as e:
        print(f"   ❌ Root endpoint error: {e}")
    
    # Test 3: Register user
    print("\n3. Testing user registration...")
    try:
        data = {
            "username": "testuser_fix",
            "password": "testpassword123"
        }
        response = requests.post(f"{BASE_URL}/api/auth/register", json=data, timeout=10)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        if response.status_code in [200, 400]:  # 400 if user already exists
            print("   ✅ Registration endpoint working")
        else:
            print("   ❌ Registration failed")
    except Exception as e:
        print(f"   ❌ Registration error: {e}")
    
    # Test 4: Login with JSON
    print("\n4. Testing login with JSON...")
    try:
        data = {
            "username": "testuser_fix",
            "password": "testpassword123"
        }
        response = requests.post(f"{BASE_URL}/api/auth/login", json=data, timeout=10)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        if response.status_code == 200:
            print("   ✅ JSON login successful!")
            token = response.json().get("access_token")
            if token:
                print(f"   Token received: {token[:20]}...")
        else:
            print("   ❌ JSON login failed")
    except Exception as e:
        print(f"   ❌ JSON login error: {e}")
    
    # Test 5: Login with form data
    print("\n5. Testing login with form data...")
    try:
        data = {
            "username": "testuser_fix",
            "password": "testpassword123"
        }
        response = requests.post(f"{BASE_URL}/api/auth/login", data=data, timeout=10)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        if response.status_code == 200:
            print("   ✅ Form data login successful!")
        else:
            print("   ❌ Form data login failed")
    except Exception as e:
        print(f"   ❌ Form data login error: {e}")
    
    # Test 6: Login with admin credentials
    print("\n6. Testing login with admin credentials...")
    try:
        data = {
            "username": "admin",
            "password": "Hk18133329@"
        }
        response = requests.post(f"{BASE_URL}/api/auth/login", json=data, timeout=10)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        if response.status_code == 200:
            print("   ✅ Admin login successful!")
        else:
            print("   ❌ Admin login failed")
    except Exception as e:
        print(f"   ❌ Admin login error: {e}")
    
    # Test 7: CORS preflight
    print("\n7. Testing CORS preflight...")
    try:
        headers = {
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "Content-Type"
        }
        response = requests.options(f"{BASE_URL}/api/auth/login", headers=headers, timeout=10)
        print(f"   Status: {response.status_code}")
        print(f"   CORS Headers: {dict(response.headers)}")
        if response.status_code == 200:
            print("   ✅ CORS preflight successful")
        else:
            print("   ❌ CORS preflight failed")
    except Exception as e:
        print(f"   ❌ CORS preflight error: {e}")

def main():
    """Main function"""
    print("Backend Fix Test Script")
    print("=" * 50)
    
    if not install_requests():
        return
    
    test_api_endpoints()
    
    print("\n" + "=" * 50)
    print("Test completed!")

if __name__ == "__main__":
    main()