#!/usr/bin/env python3
"""
Debug namespaces query
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.models import Namespace, NamespaceScope

def debug_namespaces():
    """Debug namespace query"""
    
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("DEBUG: Namespace Query")
        print("=" * 60)
        
        # Check enum values
        print("\n1. Enum Values:")
        print(f"   NamespaceScope.OFFER = {NamespaceScope.OFFER.value!r}")
        print(f"   NamespaceScope.COUPON = {NamespaceScope.COUPON.value!r}")
        print(f"   NamespaceScope.GLOBAL = {NamespaceScope.GLOBAL.value!r}")
        
        # Check all namespaces
        print("\n2. All Namespaces in DB:")
        all_ns = Namespace.query.all()
        print(f"   Total: {len(all_ns)}")
        for ns in all_ns[:5]:  # Show first 5
            print(f"   - {ns.name}: scope={ns.scope!r}, scope.value={ns.scope.value!r}")
        
        # Test the query
        print("\n3. Query with Enum:")
        result = Namespace.query.filter(
            Namespace.scope.in_([NamespaceScope.OFFER, NamespaceScope.COUPON, NamespaceScope.GLOBAL])
        ).all()
        print(f"   Results: {len(result)}")
        
        # Group by scope
        print("\n4. Grouped by Scope:")
        offer = [ns for ns in result if ns.scope == NamespaceScope.OFFER]
        coupon = [ns for ns in result if ns.scope == NamespaceScope.COUPON]
        global_ns = [ns for ns in result if ns.scope == NamespaceScope.GLOBAL]
        
        print(f"   Offer: {len(offer)}")
        print(f"   Coupon: {len(coupon)}")
        print(f"   Global: {len(global_ns)}")
        
        # Show scope values
        print("\n5. Scope Values in DB:")
        for ns in result[:5]:
            print(f"   {ns.name}: type={type(ns.scope)}, value={ns.scope.value!r}")
        
        print("\n" + "=" * 60)
        print(f"✅ Query returned {len(result)} namespaces")
        print("=" * 60)


if __name__ == '__main__':
    debug_namespaces()

