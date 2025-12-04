#!/usr/bin/env python3
"""
Script to populate default namespaces for templates
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import create_app
from app.extensions import db
from app.models import Namespace, NamespaceScope


def seed_namespaces():
    """Create default namespaces for offer templates"""
    
    app = create_app()
    
    with app.app_context():
        # Default namespaces for offers
        default_namespaces = [
            {
                'name': 'product_name',
                'label': 'Nome do Produto',
                'scope': NamespaceScope.OFFER,
                'description': 'Nome completo do produto em oferta'
            },
            {
                'name': 'price',
                'label': 'Preço',
                'scope': NamespaceScope.OFFER,
                'description': 'Preço da oferta'
            },
            {
                'name': 'old_price',
                'label': 'Preço Anterior',
                'scope': NamespaceScope.OFFER,
                'description': 'Preço antes do desconto'
            },
            {
                'name': 'discount',
                'label': 'Desconto',
                'scope': NamespaceScope.OFFER,
                'description': 'Percentual ou valor de desconto'
            },
            {
                'name': 'vendor_name',
                'label': 'Nome do Vendedor',
                'scope': NamespaceScope.OFFER,
                'description': 'Loja ou marketplace da oferta'
            },
            {
                'name': 'offer_url',
                'label': 'URL da Oferta',
                'scope': NamespaceScope.OFFER,
                'description': 'Link direto para a oferta'
            },
            {
                'name': 'category',
                'label': 'Categoria',
                'scope': NamespaceScope.OFFER,
                'description': 'Categoria do produto'
            },
            {
                'name': 'brand',
                'label': 'Marca',
                'scope': NamespaceScope.OFFER,
                'description': 'Marca ou fabricante do produto'
            },
            {
                'name': 'description',
                'label': 'Descrição',
                'scope': NamespaceScope.OFFER,
                'description': 'Descrição resumida do produto'
            },
            {
                'name': 'expires_at',
                'label': 'Validade',
                'scope': NamespaceScope.OFFER,
                'description': 'Data de expiração da oferta'
            },
            {
                'name': 'currency',
                'label': 'Moeda',
                'scope': NamespaceScope.OFFER,
                'description': 'Moeda do preço (BRL, USD, etc.)'
            },
            # Global namespaces
            {
                'name': 'user_name',
                'label': 'Nome do Usuário',
                'scope': NamespaceScope.GLOBAL,
                'description': 'Nome do usuário que está publicando'
            },
            {
                'name': 'today',
                'label': 'Data Atual',
                'scope': NamespaceScope.GLOBAL,
                'description': 'Data de hoje'
            },
            {
                'name': 'time',
                'label': 'Hora Atual',
                'scope': NamespaceScope.GLOBAL,
                'description': 'Hora atual'
            }
        ]
        
        created_count = 0
        skipped_count = 0
        
        print("🔧 Populando namespaces padrão...")
        print("-" * 50)
        
        for ns_data in default_namespaces:
            # Check if namespace already exists
            existing = Namespace.query.filter_by(name=ns_data['name']).first()
            
            if existing:
                print(f"⏭️  Namespace '{ns_data['name']}' já existe")
                skipped_count += 1
                continue
            
            # Create new namespace
            namespace = Namespace(
                name=ns_data['name'],
                label=ns_data['label'],
                scope=ns_data['scope'],
                description=ns_data['description']
            )
            
            db.session.add(namespace)
            created_count += 1
            print(f"✅ Criado: {ns_data['name']} ({ns_data['label']})")
        
        # Commit changes
        db.session.commit()
        
        print("-" * 50)
        print(f"\n📊 Resumo:")
        print(f"   ✅ Criados: {created_count}")
        print(f"   ⏭️  Já existiam: {skipped_count}")
        print(f"   📦 Total: {Namespace.query.count()}")
        print("\n🎉 Namespaces populados com sucesso!")


if __name__ == "__main__":
    seed_namespaces()

