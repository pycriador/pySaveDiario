#!/usr/bin/env python3
"""
Test script for TemplateSocialNetwork model and routes
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_model():
    """Test if model loads correctly"""
    print("🧪 Testando modelo TemplateSocialNetwork...")
    
    try:
        from app.models import TemplateSocialNetwork, Template
        print("✅ Modelo importado com sucesso!")
        print(f"   Tabela: {TemplateSocialNetwork.__tablename__}")
        
        from app import create_app, db
        app = create_app()
        
        with app.app_context():
            # Check if any templates exist
            templates = Template.query.all()
            print(f"✅ Templates no banco: {len(templates)}")
            
            if templates:
                template = templates[0]
                print(f"   Template de teste: {template.name} (ID: {template.id})")
                
                # Try to create a test custom template
                test_custom = TemplateSocialNetwork(
                    template_id=template.id,
                    social_network='test',
                    custom_body='Test body'
                )
                
                print(f"✅ Objeto criado: {test_custom}")
                print(f"   to_dict(): {test_custom.to_dict()}")
                
                # Don't save to DB, just test object creation
                print("\n✅ Todos os testes passaram!")
            else:
                print("⚠️  Nenhum template encontrado no banco para testar")
                
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_model()

