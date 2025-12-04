#!/usr/bin/env python3
"""
Add coupon-specific namespaces
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.extensions import db
from app.models import Namespace, NamespaceScope


def add_coupon_namespaces():
    """Add coupon-specific namespaces"""
    
    app = create_app()
    
    with app.app_context():
        coupon_namespaces = [
            {
                'name': 'coupon_code',
                'label': 'Código do Cupom',
                'description': 'Código do cupom de desconto',
                'example': 'PRIMEIRACOMPRA',
                'scope': NamespaceScope.COUPON
            },
            {
                'name': 'code',
                'label': 'Código (Alias)',
                'description': 'Código do cupom (forma abreviada)',
                'example': 'FRETE10',
                'scope': NamespaceScope.COUPON
            },
            {
                'name': 'seller',
                'label': 'Vendedor',
                'description': 'Nome do vendedor/loja do cupom',
                'example': 'Mercado Livre',
                'scope': NamespaceScope.COUPON
            },
            {
                'name': 'seller_name',
                'label': 'Nome do Vendedor',
                'description': 'Nome do vendedor (forma longa)',
                'example': 'Magazine Luiza',
                'scope': NamespaceScope.COUPON
            },
            {
                'name': 'coupon_expires',
                'label': 'Validade do Cupom',
                'description': 'Data de expiração do cupom',
                'example': '31/12/2025',
                'scope': NamespaceScope.COUPON
            }
        ]
        
        for ns_data in coupon_namespaces:
            existing = Namespace.query.filter_by(
                name=ns_data['name'], 
                scope=ns_data['scope']
            ).first()
            
            if not existing:
                namespace = Namespace(**ns_data)
                db.session.add(namespace)
                print(f"✓ Created namespace: {ns_data['name']} ({ns_data['scope'].value})")
            else:
                print(f"⊘ Namespace already exists: {ns_data['name']} ({ns_data['scope'].value})")
        
        db.session.commit()
        print("\n✅ Coupon namespaces added successfully!")


if __name__ == '__main__':
    add_coupon_namespaces()

