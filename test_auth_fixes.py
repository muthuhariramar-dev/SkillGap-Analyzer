#!/usr/bin/env python3
"""
Test script to verify login and registration fixes
"""

import requests
import json

# Base URLs
BACKEND_URL = "http://localhost:8000"

def test_registration():
    """Test user registration"""
    print("🔧 Testing Registration...")
    print("-" * 40)
    
    # Test data
    registration_data = {
        "fullName": "Test User",
        "email": "testuser@example.com",
        "password": "password123",
        "userType": "student"
    }
    
    try:
        response = requests.post(f"{BACKEND_URL}/api/auth/register", 
                               json=registration_data,
                               headers={"Content-Type": "application/json"})
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            print("✅ Registration successful!")
            return response.json().get('token')
        else:
            print("❌ Registration failed!")
            return None
            
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return None

def test_login():
    """Test user login"""
    print("\n🔐 Testing Login...")
    print("-" * 40)
    
    # Test data
    login_data = {
        "email": "testuser@example.com",
        "password": "password123"
    }
    
    try:
        response = requests.post(f"{BACKEND_URL}/api/auth/login", 
                               json=login_data,
                               headers={"Content-Type": "application/json"})
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            print("✅ Login successful!")
            return response.json().get('token')
        else:
            print("❌ Login failed!")
            return None
            
    except Exception as e:
        print(f"❌ Login error: {e}")
        return None

def test_existing_user_login():
    """Test login with existing user"""
    print("\n👤 Testing Existing User Login...")
    print("-" * 40)
    
    # Use existing test user
    login_data = {
        "email": "samykmottaya@gmail.com",
        "password": "Danger!123"
    }
    
    try:
        response = requests.post(f"{BACKEND_URL}/api/auth/login", 
                               json=login_data,
                               headers={"Content-Type": "application/json"})
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            print("✅ Existing user login successful!")
            return response.json().get('token')
        else:
            print("❌ Existing user login failed!")
            return None
            
    except Exception as e:
        print(f"❌ Existing user login error: {e}")
        return None

def test_token_validation(token):
    """Test token validation"""
    if not token:
        print("\n⚠️ Skipping token validation (no token)")
        return
        
    print("\n🔍 Testing Token Validation...")
    print("-" * 40)
    
    try:
        response = requests.get(f"{BACKEND_URL}/api/auth/validate", 
                              headers={"Authorization": f"Bearer {token}"})
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            print("✅ Token validation successful!")
        else:
            print("❌ Token validation failed!")
            
    except Exception as e:
        print(f"❌ Token validation error: {e}")

def main():
    print("🚀 Authentication System Test")
    print("=" * 50)
    
    # Test 1: Registration
    token = test_registration()
    
    # Test 2: Login with new user
    token = test_login()
    
    # Test 3: Token validation
    test_token_validation(token)
    
    # Test 4: Existing user login
    existing_token = test_existing_user_login()
    
    # Test 5: Existing user token validation
    test_token_validation(existing_token)
    
    print("\n🎉 Authentication tests completed!")

if __name__ == "__main__":
    main()
