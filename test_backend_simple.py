#!/usr/bin/env python3
"""
Simple test to verify backend is working
"""

import requests
import json

def test_backend():
    try:
        # Test basic endpoint
        response = requests.get('http://localhost:8000/api/test')
        if response.status_code == 200:
            print("✅ Backend is running and accessible")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ Backend returned status: {response.status_code}")
    except Exception as e:
        print(f"❌ Backend connection error: {e}")

if __name__ == "__main__":
    test_backend()
