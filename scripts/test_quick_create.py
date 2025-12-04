#!/usr/bin/env python3
"""
Test script for quick create API endpoints
"""
import requests
import json

BASE_URL = "http://localhost:5000"

# You need to be logged in - get the session cookie from your browser
# This is just for testing

def test_create_category():
    """Test creating a category"""
    url = f"{BASE_URL}/api/categories"
    
    data = {
        "name": "Test Category",
        "slug": "test-category",
        "active": True
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    print(f"Testing POST {url}")
    print(f"Data: {json.dumps(data, indent=2)}")
    
    # Note: This will fail if you're not logged in
    # You need to copy your session cookie from the browser
    response = requests.post(url, json=data, headers=headers)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.ok:
        print("✅ Success!")
        return response.json()
    else:
        print("❌ Failed!")
        return None

def test_create_seller():
    """Test creating a seller"""
    url = f"{BASE_URL}/api/sellers"
    
    data = {
        "name": "Test Seller",
        "slug": "test-seller",
        "active": True
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    print(f"\nTesting POST {url}")
    print(f"Data: {json.dumps(data, indent=2)}")
    
    response = requests.post(url, json=data, headers=headers)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.ok:
        print("✅ Success!")
        return response.json()
    else:
        print("❌ Failed!")
        return None

def test_create_manufacturer():
    """Test creating a manufacturer"""
    url = f"{BASE_URL}/api/manufacturers"
    
    data = {
        "name": "Test Manufacturer",
        "slug": "test-manufacturer",
        "active": True
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    print(f"\nTesting POST {url}")
    print(f"Data: {json.dumps(data, indent=2)}")
    
    response = requests.post(url, json=data, headers=headers)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.ok:
        print("✅ Success!")
        return response.json()
    else:
        print("❌ Failed!")
        return None

if __name__ == "__main__":
    print("=" * 60)
    print("Testing Quick Create API Endpoints")
    print("=" * 60)
    print("\nNOTE: You must be logged in for these tests to work.")
    print("The tests will fail with 401 if not authenticated.\n")
    
    # Test all endpoints
    test_create_category()
    test_create_seller()
    test_create_manufacturer()
    
    print("\n" + "=" * 60)
    print("Tests Complete")
    print("=" * 60)

