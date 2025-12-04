#!/usr/bin/env python3
"""
Add min_purchase_value column to coupons table
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import create_app, db
from sqlalchemy import text

def add_min_purchase_value_column():
    """Add min_purchase_value column to coupons table"""
    app = create_app()
    
    with app.app_context():
        try:
            # Check if column already exists
            result = db.session.execute(text("PRAGMA table_info(coupons)"))
            columns = [row[1] for row in result.fetchall()]
            
            if 'min_purchase_value' in columns:
                print("✓ Coluna 'min_purchase_value' já existe na tabela 'coupons'")
                return
            
            # Add the column
            db.session.execute(text(
                "ALTER TABLE coupons ADD COLUMN min_purchase_value NUMERIC(10, 2)"
            ))
            db.session.commit()
            
            print("✅ Coluna 'min_purchase_value' adicionada com sucesso à tabela 'coupons'!")
            print("\nDescrição: Valor mínimo da compra para aplicar o cupom")
            
        except Exception as e:
            print(f"❌ Erro ao adicionar coluna: {e}")
            db.session.rollback()

if __name__ == '__main__':
    add_min_purchase_value_column()

