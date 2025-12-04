#!/usr/bin/env python3
"""
Reorganize and add clearer coupon namespaces
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import create_app, db
from app.models import Namespace, NamespaceScope

def reorganize_coupon_namespaces():
    """Add clearer namespace names in Portuguese"""
    app = create_app()
    
    with app.app_context():
        namespaces_to_add = [
            # Porcentagem do desconto (clearer names)
            {
                'name': 'porcentagem',
                'label': 'Porcentagem do Desconto',
                'scope': NamespaceScope.COUPON,
                'description': 'Valor do desconto quando é porcentagem (ex: 10%)'
            },
            {
                'name': 'desconto_porcentagem',
                'label': 'Desconto em Porcentagem',
                'scope': NamespaceScope.COUPON,
                'description': 'Alias para porcentagem do desconto'
            },
            {
                'name': 'percentual',
                'label': 'Percentual de Desconto',
                'scope': NamespaceScope.COUPON,
                'description': 'Alias para porcentagem'
            },
            
            # Valor mínimo da compra (clearer names)
            {
                'name': 'valor_minimo_compra',
                'label': 'Valor Mínimo da Compra',
                'scope': NamespaceScope.COUPON,
                'description': 'Valor mínimo que o cliente precisa comprar'
            },
            {
                'name': 'minimo',
                'label': 'Mínimo',
                'scope': NamespaceScope.COUPON,
                'description': 'Alias curto para valor mínimo'
            },
            
            # Valor máximo do desconto (clearer names)
            {
                'name': 'valor_maximo_desconto',
                'label': 'Valor Máximo do Desconto',
                'scope': NamespaceScope.COUPON,
                'description': 'Limite máximo de desconto em R$'
            },
            {
                'name': 'maximo',
                'label': 'Máximo',
                'scope': NamespaceScope.COUPON,
                'description': 'Alias curto para valor máximo'
            },
            {
                'name': 'limite',
                'label': 'Limite de Desconto',
                'scope': NamespaceScope.COUPON,
                'description': 'Alias para limite máximo de desconto'
            },
            
            # Desconto em valor fixo
            {
                'name': 'desconto_fixo',
                'label': 'Desconto Fixo (R$)',
                'scope': NamespaceScope.COUPON,
                'description': 'Valor do desconto quando é fixo em reais'
            },
            {
                'name': 'valor_fixo',
                'label': 'Valor Fixo do Desconto',
                'scope': NamespaceScope.COUPON,
                'description': 'Alias para desconto fixo'
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
                print(f"✅ Adicionado: {ns_data['name']} - {ns_data['label']}")
                added_count += 1
        
        if added_count > 0:
            db.session.commit()
            print(f"\n🎉 {added_count} namespace(s) adicionado(s) com sucesso!")
        else:
            print(f"\n✓ Todos os namespaces já existiam")

if __name__ == '__main__':
    reorganize_coupon_namespaces()

