#!/usr/bin/env python3
"""
Add global namespaces for user contact information
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import create_app, db
from app.models import Namespace, NamespaceScope

def add_user_global_namespaces():
    """Add global namespaces for user information"""
    app = create_app()
    
    with app.app_context():
        namespaces_to_add = [
            # Contact info
            {
                'name': 'user_phone',
                'label': 'Celular do Usuário',
                'scope': NamespaceScope.GLOBAL,
                'description': 'Número de telefone/celular do usuário criador'
            },
            {
                'name': 'telefone',
                'label': 'Telefone (Alias)',
                'scope': NamespaceScope.GLOBAL,
                'description': 'Alias para telefone do usuário'
            },
            {
                'name': 'celular',
                'label': 'Celular (Alias)',
                'scope': NamespaceScope.GLOBAL,
                'description': 'Alias para celular do usuário'
            },
            {
                'name': 'user_address',
                'label': 'Endereço do Usuário',
                'scope': NamespaceScope.GLOBAL,
                'description': 'Endereço do usuário criador'
            },
            {
                'name': 'endereco',
                'label': 'Endereço (Alias)',
                'scope': NamespaceScope.GLOBAL,
                'description': 'Alias para endereço do usuário'
            },
            {
                'name': 'user_website',
                'label': 'Website do Usuário',
                'scope': NamespaceScope.GLOBAL,
                'description': 'Website/blog do usuário criador'
            },
            {
                'name': 'site',
                'label': 'Site (Alias)',
                'scope': NamespaceScope.GLOBAL,
                'description': 'Alias para website do usuário'
            },
            
            # Social media
            {
                'name': 'user_instagram',
                'label': 'Instagram do Usuário',
                'scope': NamespaceScope.GLOBAL,
                'description': 'Perfil do Instagram do usuário (@usuario ou URL)'
            },
            {
                'name': 'instagram',
                'label': 'Instagram (Alias)',
                'scope': NamespaceScope.GLOBAL,
                'description': 'Alias para Instagram do usuário'
            },
            {
                'name': 'user_facebook',
                'label': 'Facebook do Usuário',
                'scope': NamespaceScope.GLOBAL,
                'description': 'Perfil do Facebook do usuário'
            },
            {
                'name': 'facebook',
                'label': 'Facebook (Alias)',
                'scope': NamespaceScope.GLOBAL,
                'description': 'Alias para Facebook do usuário'
            },
            {
                'name': 'user_twitter',
                'label': 'Twitter/X do Usuário',
                'scope': NamespaceScope.GLOBAL,
                'description': 'Perfil do Twitter/X do usuário (@usuario ou URL)'
            },
            {
                'name': 'twitter',
                'label': 'Twitter (Alias)',
                'scope': NamespaceScope.GLOBAL,
                'description': 'Alias para Twitter do usuário'
            },
            {
                'name': 'user_linkedin',
                'label': 'LinkedIn do Usuário',
                'scope': NamespaceScope.GLOBAL,
                'description': 'Perfil do LinkedIn do usuário'
            },
            {
                'name': 'linkedin',
                'label': 'LinkedIn (Alias)',
                'scope': NamespaceScope.GLOBAL,
                'description': 'Alias para LinkedIn do usuário'
            },
            {
                'name': 'user_youtube',
                'label': 'YouTube do Usuário',
                'scope': NamespaceScope.GLOBAL,
                'description': 'Canal do YouTube do usuário'
            },
            {
                'name': 'youtube',
                'label': 'YouTube (Alias)',
                'scope': NamespaceScope.GLOBAL,
                'description': 'Alias para YouTube do usuário'
            },
            {
                'name': 'user_tiktok',
                'label': 'TikTok do Usuário',
                'scope': NamespaceScope.GLOBAL,
                'description': 'Perfil do TikTok do usuário (@usuario ou URL)'
            },
            {
                'name': 'tiktok',
                'label': 'TikTok (Alias)',
                'scope': NamespaceScope.GLOBAL,
                'description': 'Alias para TikTok do usuário'
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
    add_user_global_namespaces()

