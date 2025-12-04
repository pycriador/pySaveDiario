#!/usr/bin/env python3
"""
Add min_purchase_value namespaces to database
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import create_app, db
from app.models import Namespace, NamespaceScope

def add_min_purchase_namespaces():
    """Add min_purchase_value related namespaces"""
    app = create_app()
    
    with app.app_context():
        namespaces_to_add = [
            {
                'name': 'min_purchase_value',
                'label': 'Valor Mínimo da Compra',
                'scope': NamespaceScope.COUPON,
                'description': 'Valor mínimo para aplicar o cupom (ex: R$ 100)'
            },
            {
                'name': 'compra_minima',
                'label': 'Compra Mínima (Alias)',
                'scope': NamespaceScope.COUPON,
                'description': 'Alias para valor mínimo da compra'
            },
            {
                'name': 'valor_minimo',
                'label': 'Valor Mínimo (Alias)',
                'scope': NamespaceScope.COUPON,
                'description': 'Alias para valor mínimo da compra'
            },
        ]
        
        added_count = 0
        
        for ns_data in namespaces_to_add:
            existing = Namespace.query.filter_by(
                name=ns_data['name'],
                scope=ns_data['scope']
            ).first()
            
            if existing:
                print(f"✓ Namespace '{ns_data['name']}' já existe")
            else:
                new_namespace = Namespace(**ns_data)
                db.session.add(new_namespace)
                print(f"✓ Adicionado namespace: {ns_data['name']} ({ns_data['label']})")
                added_count += 1
        
        if added_count > 0:
            db.session.commit()
            print(f"\n✅ {added_count} namespace(s) adicionado(s) com sucesso!")
        else:
            print(f"\n✓ Nenhum namespace novo adicionado (todos já existiam)")

if __name__ == '__main__':
    add_min_purchase_namespaces()

