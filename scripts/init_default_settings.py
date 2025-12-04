#!/usr/bin/env python3
"""
Initialize default application settings
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app import create_app
from app.extensions import db
from app.models import AppSettings


def init_settings():
    """Initialize default settings"""
    app = create_app()
    
    with app.app_context():
        print("🔧 Inicializando configurações padrão...")
        print("-" * 50)
        
        # Check if default_currency already exists
        existing = AppSettings.query.filter_by(key='default_currency').first()
        
        if existing:
            print(f"⏭️  Moeda padrão já configurada: {existing.value}")
        else:
            # Create default currency setting
            setting = AppSettings(
                key='default_currency',
                value='BRL',
                description='Moeda padrão do sistema'
            )
            db.session.add(setting)
            db.session.commit()
            print(f"✅ Moeda padrão configurada: BRL")
        
        print("-" * 50)
        print("🎉 Configurações inicializadas!")


if __name__ == "__main__":
    init_settings()

