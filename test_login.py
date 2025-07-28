#!/usr/bin/env python3
"""
Test script for login functionality
"""

import requests
import json

# Base URL - change this to your Heroku app URL
BASE_URL = "https://hakon-56ae06ddc8d1.herokuapp.com"

def test_register():
    """Test user registration"""
    url = f"{BASE_URL}/api/auth/register"
    data = {
        "username": "testuser",
        "password": "testpassword123"
    }
    
    print("Testing user registration...")
    response = requests.post(url, json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    return response.status_code == 200

def test_login_json():
    """Test login with JSON data"""
    url = f"{BASE_URL}/api/auth/login-json"
    data = {
        "username": "testuser",
        "password": "testpassword123"
    }
    
    print("\nTesting login with JSON...")
    response = requests.post(url, json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    return response.status_code == 200

def test_login_form():
    """Test login with form data"""
    url = f"{BASE_URL}/api/auth/login"
    data = {
        "username": "testuser",
        "password": "testpassword123"
    }
    
    print("\nTesting login with form data...")
    response = requests.post(url, data=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    return response.status_code == 200

def test_health():
    """Test health endpoint"""
    url = f"{BASE_URL}/health"
    
    print("\nTesting health endpoint...")
    response = requests.get(url)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")

if __name__ == "__main__":
    print("=== Login Test Script ===")
    
    # Test health first
    test_health()
    
    # Test registration
    if test_register():
        print("\n✅ Registration successful!")
        
        # Test both login methods
        json_success = test_login_json()
        form_success = test_login_form()
        
        if json_success:
            print("\n✅ JSON login successful!")
        else:
            print("\n❌ JSON login failed!")
            
        if form_success:
            print("\n✅ Form login successful!")
        else:
            print("\n❌ Form login failed!")
    else:
        print("\n❌ Registration failed!")