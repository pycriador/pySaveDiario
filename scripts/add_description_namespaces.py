#!/usr/bin/env python
"""
Add product description namespaces

These namespaces allow using HTML descriptions in templates,
which are automatically converted to formatted text for each social network.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import Namespace, NamespaceScope

def add_description_namespaces():
    """Add product description namespaces"""
    app = create_app()
    
    with app.app_context():
        try:
            namespaces_to_add = [
                {
                    'name': 'product_description',
                    'label': 'Descrição do Produto',
                    'description': 'Descrição completa do produto (converte HTML para texto formatado)',
                    'scope': NamespaceScope.OFFER
                },
                {
                    'name': 'description',
                    'label': 'Descrição',
                    'description': 'Descrição do produto (atalho)',
                    'scope': NamespaceScope.OFFER
                },
                {
                    'name': 'descricao',
                    'label': 'Descrição (PT)',
                    'description': 'Descrição do produto em português',
                    'scope': NamespaceScope.OFFER
                }
            ]
            
            added = []
            for ns_data in namespaces_to_add:
                existing = Namespace.query.filter_by(name=ns_data['name']).first()
                if not existing:
                    namespace = Namespace(**ns_data)
                    db.session.add(namespace)
                    added.append(ns_data['name'])
                    print(f"➕ Added namespace: {{{ns_data['name']}}}")
                else:
                    print(f"✓ Namespace already exists: {{{ns_data['name']}}}")
            
            if added:
                db.session.commit()
                print(f"\n✅ Successfully added {len(added)} namespace(s)!")
                print("\n📝 Usage in templates:")
                print("   {product_description} - Descrição completa do produto")
                print("   {description} - Atalho para descrição")
                print("   {descricao} - Versão em português")
                print("\n💡 Formatting by network:")
                print("   WhatsApp: *bold*, _italic_, ~strikethrough~")
                print("   Telegram: **bold**, __italic__, ~~strikethrough~~")
                print("   Instagram/Facebook: Plain text with line breaks")
            else:
                print("\n✓ All namespaces already exist. No changes made.")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            db.session.rollback()
            raise

if __name__ == "__main__":
    add_description_namespaces()

