#!/usr/bin/env python3
"""
Debug script for quick create routes
"""
from app import create_app
from app.models import User
from flask import json

app = create_app()

with app.test_client() as client:
    # Login first
    print("=" * 60)
    print("TESTE: Quick Create Categories")
    print("=" * 60)
    
    # Get any user
    with app.app_context():
        admin = User.query.first()
        if not admin:
            print("❌ No users found. Create one first:")
            print("   python scripts/create_admin.py")
            exit(1)
        print(f"✅ Found user: {admin.email} (role: {admin.role.value})")
    
    # Login
    print("\n1️⃣  Logging in...")
    response = client.post('/login', data={
        'email': admin.email,
        'password': 'admin'  # Default password
    }, follow_redirects=False)
    
    if response.status_code in [200, 302]:
        print(f"✅ Login successful (status: {response.status_code})")
    else:
        print(f"❌ Login failed (status: {response.status_code})")
        exit(1)
    
    # Test quick create
    print("\n2️⃣  Testing POST /quick-create/categories...")
    response = client.post('/quick-create/categories',
        json={
            'name': 'Test Category Debug',
            'slug': 'test-category-debug',
            'active': True
        },
        content_type='application/json'
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Content-Type: {response.content_type}")
    print(f"Response Data: {response.data.decode('utf-8')[:500]}")
    
    if response.status_code == 201:
        data = response.get_json()
        print(f"\n✅ SUCCESS! Category created:")
        print(f"   ID: {data['id']}")
        print(f"   Name: {data['name']}")
        print(f"   Slug: {data['slug']}")
    else:
        print(f"\n❌ FAILED!")
        if 'application/json' in response.content_type:
            error = response.get_json()
            print(f"   Error: {error.get('error', 'Unknown error')}")
        else:
            print("   Response is not JSON (probably HTML error page)")
            print(f"   First 500 chars:\n{response.data.decode('utf-8')[:500]}")
    
    print("\n" + "=" * 60)

