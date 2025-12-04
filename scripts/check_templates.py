"""
Script to check templates in the database
Useful for debugging template creation issues
"""

import sys
import os

# Add parent directory to path to import app modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import Template

def check_templates():
    """Check and display all templates in the database"""
    app = create_app()
    
    with app.app_context():
        templates = Template.query.all()
        
        print("=" * 70)
        print("📋 Templates no Banco de Dados")
        print("=" * 70)
        
        if not templates:
            print("\n⚠️  Nenhum template encontrado no banco de dados")
            print("\n💡 Isso pode significar:")
            print("   1. Nenhum template foi criado ainda")
            print("   2. O template foi criado mas não foi commitado")
            print("   3. Você está olhando o banco de dados errado")
            return
        
        print(f"\n✅ Total de templates: {len(templates)}\n")
        
        for i, template in enumerate(templates, 1):
            print(f"{i}. {template.name}")
            print(f"   ID: {template.id}")
            print(f"   Slug: {template.slug}")
            print(f"   Descrição: {template.description or 'N/A'}")
            print(f"   Canais: {template.channels}")
            print(f"   Corpo: {template.body[:100]}..." if len(template.body) > 100 else f"   Corpo: {template.body}")
            print(f"   Criado em: {template.created_at}")
            print(f"   Atualizado em: {template.updated_at}")
            print()
        
        # Check database file location
        print("=" * 70)
        print("📁 Informações do Banco de Dados")
        print("=" * 70)
        print(f"Database URI: {app.config.get('SQLALCHEMY_DATABASE_URI')}")
        print()


def create_test_template():
    """Create a test template for debugging"""
    app = create_app()
    
    with app.app_context():
        # Check if test template already exists
        existing = Template.query.filter_by(slug='template-teste').first()
        if existing:
            print("⚠️  Template de teste já existe. Deletando...")
            db.session.delete(existing)
            db.session.commit()
        
        # Create test template
        test_template = Template(
            name="Template de Teste",
            slug="template-teste",
            description="Este é um template criado automaticamente para teste",
            body="Olá! Este é o corpo do template de teste.\n\nPode deletar este template.",
            channels="instagram,facebook,whatsapp"
        )
        
        db.session.add(test_template)
        db.session.commit()
        
        print("=" * 70)
        print("✅ Template de Teste Criado com Sucesso!")
        print("=" * 70)
        print(f"Nome: {test_template.name}")
        print(f"Slug: {test_template.slug}")
        print(f"ID: {test_template.id}")
        print()
        print("💡 Acesse /templates no navegador para ver o template")
        print("💡 Execute 'python scripts/check_templates.py' para listar todos")
        print()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Check or create templates")
    parser.add_argument('--create-test', action='store_true', help='Create a test template')
    args = parser.parse_args()
    
    if args.create_test:
        create_test_template()
    else:
        check_templates()

