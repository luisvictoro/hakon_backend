#!/usr/bin/env python3
"""
Simple test script to verify login fix
"""

import requests
import json

# Base URL
BASE_URL = "https://hakon-56ae06ddc8d1.herokuapp.com"

def test_login():
    """Test the fixed login endpoint"""
    url = f"{BASE_URL}/api/auth/login"
    
    # Test data
    data = {
        "username": "admin",
        "password": "admin"
    }
    
    print("Testing login endpoint...")
    print(f"URL: {url}")
    print(f"Data: {json.dumps(data, indent=2)}")
    
    try:
        response = requests.post(url, json=data, timeout=10)
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Body: {response.text}")
        
        if response.status_code == 200:
            print("\n✅ Login successful!")
            token_data = response.json()
            if "access_token" in token_data:
                print(f"Token received: {token_data['access_token'][:20]}...")
            return True
        elif response.status_code == 422:
            print("\n❌ Validation error - check request format")
            return False
        elif response.status_code == 401:
            print("\n❌ Authentication failed - check username/password")
            return False
        else:
            print(f"\n❌ Unexpected status code: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Request error: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return False

def test_health():
    """Test health endpoint"""
    url = f"{BASE_URL}/health"
    
    print("\nTesting health endpoint...")
    try:
        response = requests.get(url, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check error: {e}")
        return False

if __name__ == "__main__":
    print("=== Login Fix Test ===")
    
    # Test health first
    if test_health():
        print("✅ Health check passed")
        
        # Test login
        if test_login():
            print("\n🎉 Login fix is working!")
        else:
            print("\n❌ Login still has issues")
    else:
        print("❌ Health check failed - app may be down")