#!/usr/bin/env python3
"""
Test script for local backend
"""

import requests
import json
import time

def test_local_backend():
    """Test local backend endpoints"""
    BASE_URL = "http://localhost:8000"
    
    print("=== Testing Local Backend ===\n")
    
    # Test 1: Health check
    print("1. Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        if response.status_code == 200:
            print("   ✅ Health check passed")
        else:
            print("   ❌ Health check failed")
    except Exception as e:
        print(f"   ❌ Health check error: {e}")
        print("   Make sure the backend is running with: uvicorn app.main:app --reload")
        return
    
    # Test 2: Register user
    print("\n2. Testing user registration...")
    try:
        data = {
            "username": "testuser_local",
            "password": "testpassword123"
        }
        response = requests.post(f"{BASE_URL}/api/auth/register", json=data, timeout=5)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        if response.status_code in [200, 400]:  # 400 if user already exists
            print("   ✅ Registration endpoint working")
        else:
            print("   ❌ Registration failed")
    except Exception as e:
        print(f"   ❌ Registration error: {e}")
    
    # Test 3: Login with JSON
    print("\n3. Testing login with JSON...")
    try:
        data = {
            "username": "testuser_local",
            "password": "testpassword123"
        }
        response = requests.post(f"{BASE_URL}/api/auth/login", json=data, timeout=5)
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
    
    # Test 4: Login with form data
    print("\n4. Testing login with form data...")
    try:
        data = {
            "username": "testuser_local",
            "password": "testpassword123"
        }
        response = requests.post(f"{BASE_URL}/api/auth/login", data=data, timeout=5)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        if response.status_code == 200:
            print("   ✅ Form data login successful!")
        else:
            print("   ❌ Form data login failed")
    except Exception as e:
        print(f"   ❌ Form data login error: {e}")
    
    # Test 5: CORS preflight
    print("\n5. Testing CORS preflight...")
    try:
        headers = {
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "Content-Type"
        }
        response = requests.options(f"{BASE_URL}/api/auth/login", headers=headers, timeout=5)
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
    print("Local Backend Test Script")
    print("=" * 50)
    print("Make sure the backend is running with:")
    print("uvicorn app.main:app --reload")
    print("=" * 50)
    
    test_local_backend()
    
    print("\n" + "=" * 50)
    print("Test completed!")

if __name__ == "__main__":
    main()