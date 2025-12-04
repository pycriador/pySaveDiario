#!/usr/bin/env python3
"""
Add contact and social media fields to users table
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import create_app, db
from sqlalchemy import text

def add_user_contact_fields():
    """Add phone, address, website and social media fields to users table"""
    app = create_app()
    
    with app.app_context():
        # Check existing columns
        result = db.session.execute(text("PRAGMA table_info(users)"))
        existing_columns = [row[1] for row in result.fetchall()]
        
        fields_to_add = [
            ('phone', 'VARCHAR(20)'),
            ('address', 'VARCHAR(255)'),
            ('website', 'VARCHAR(255)'),
            ('instagram', 'VARCHAR(255)'),
            ('facebook', 'VARCHAR(255)'),
            ('twitter', 'VARCHAR(255)'),
            ('linkedin', 'VARCHAR(255)'),
            ('youtube', 'VARCHAR(255)'),
            ('tiktok', 'VARCHAR(255)'),
        ]
        
        added_count = 0
        
        for field_name, field_type in fields_to_add:
            if field_name in existing_columns:
                print(f"✓ Campo '{field_name}' já existe")
            else:
                try:
                    db.session.execute(text(
                        f"ALTER TABLE users ADD COLUMN {field_name} {field_type}"
                    ))
                    db.session.commit()
                    print(f"✅ Campo '{field_name}' adicionado com sucesso!")
                    added_count += 1
                except Exception as e:
                    print(f"❌ Erro ao adicionar '{field_name}': {e}")
                    db.session.rollback()
        
        if added_count > 0:
            print(f"\n🎉 Total: {added_count} campo(s) adicionado(s)!")
        else:
            print(f"\n✓ Todos os campos já existiam")

if __name__ == '__main__':
    add_user_contact_fields()

