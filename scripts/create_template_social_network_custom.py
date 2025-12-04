#!/usr/bin/env python3
"""
Create template_social_network_custom table for storing custom template bodies per social network
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import create_app, db
from sqlalchemy import text

def create_template_social_network_custom():
    """Create template_social_network_custom table"""
    app = create_app()
    
    with app.app_context():
        # Check if table already exists
        result = db.session.execute(text(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='template_social_network_custom'"
        ))
        
        if result.fetchone():
            print("✓ Tabela 'template_social_network_custom' já existe")
            return
        
        # Create table
        try:
            db.session.execute(text("""
                CREATE TABLE template_social_network_custom (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    template_id INTEGER NOT NULL,
                    social_network VARCHAR(50) NOT NULL,
                    custom_body TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (template_id) REFERENCES templates(id) ON DELETE CASCADE,
                    CONSTRAINT uq_template_social_network UNIQUE (template_id, social_network)
                )
            """))
            
            # Create index for faster lookups
            db.session.execute(text("""
                CREATE INDEX idx_template_social_network_custom_template_id 
                ON template_social_network_custom(template_id)
            """))
            
            db.session.execute(text("""
                CREATE INDEX idx_template_social_network_custom_social_network 
                ON template_social_network_custom(social_network)
            """))
            
            db.session.commit()
            print("✅ Tabela 'template_social_network_custom' criada com sucesso!")
            print("✅ Índices criados com sucesso!")
            
        except Exception as e:
            print(f"❌ Erro ao criar tabela: {e}")
            db.session.rollback()

if __name__ == '__main__':
    create_template_social_network_custom()

