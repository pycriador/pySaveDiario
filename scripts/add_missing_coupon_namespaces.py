#!/usr/bin/env python3
"""
Add missing coupon namespaces to database
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import create_app, db
from app.models import Namespace, NamespaceScope

def add_missing_namespaces():
    """Add missing coupon-related namespaces"""
    app = create_app()
    
    with app.app_context():
        namespaces_to_add = [
            # Discount type
            {
                'name': 'coupon_discount_type',
                'label': 'Tipo de Desconto do Cupom',
                'scope': NamespaceScope.COUPON,
                'description': 'Tipo de desconto (percentage ou fixed)'
            },
            {
                'name': 'tipo_desconto',
                'label': 'Tipo de Desconto (Alias)',
                'scope': NamespaceScope.COUPON,
                'description': 'Alias para tipo de desconto'
            },
            # Discount value
            {
                'name': 'coupon_discount_value',
                'label': 'Valor do Desconto',
                'scope': NamespaceScope.COUPON,
                'description': 'Valor do desconto (% ou R$)'
            },
            {
                'name': 'valor_desconto',
                'label': 'Valor do Desconto (Alias)',
                'scope': NamespaceScope.COUPON,
                'description': 'Alias para valor do desconto'
            },
            # Max discount value
            {
                'name': 'max_discount_value',
                'label': 'Limite Máximo de Desconto',
                'scope': NamespaceScope.COUPON,
                'description': 'Valor máximo de desconto do cupom (ex: R$ 50)'
            },
            {
                'name': 'limite_desconto',
                'label': 'Limite de Desconto (Alias)',
                'scope': NamespaceScope.COUPON,
                'description': 'Alias para limite máximo de desconto'
            },
            {
                'name': 'coupon_max_discount',
                'label': 'Desconto Máximo do Cupom',
                'scope': NamespaceScope.COUPON,
                'description': 'Desconto máximo permitido pelo cupom'
            },
            # Expires at (alternate names to avoid conflict)
            {
                'name': 'validade_cupom',
                'label': 'Validade do Cupom',
                'scope': NamespaceScope.COUPON,
                'description': 'Data de validade/expiração do cupom'
            },
            {
                'name': 'expira_em',
                'label': 'Data de Expiração',
                'scope': NamespaceScope.COUPON,
                'description': 'Data em que o cupom expira'
            },
        ]
        
        added_count = 0
        updated_count = 0
        
        for ns_data in namespaces_to_add:
            existing = Namespace.query.filter_by(
                name=ns_data['name'],
                scope=ns_data['scope']
            ).first()
            
            if existing:
                print(f"✓ Namespace '{ns_data['name']}' já existe")
                updated_count += 1
            else:
                new_namespace = Namespace(**ns_data)
                db.session.add(new_namespace)
                print(f"✓ Adicionado namespace: {ns_data['name']} ({ns_data['label']})")
                added_count += 1
        
        if added_count > 0:
            db.session.commit()
            print(f"\n✅ {added_count} namespace(s) adicionado(s) com sucesso!")
        else:
            print(f"\n✓ Nenhum namespace novo adicionado ({updated_count} já existiam)")

if __name__ == '__main__':
    add_missing_namespaces()

