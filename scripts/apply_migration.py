#!/usr/bin/env python3
"""
Apply pending migrations
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from flask_migrate import upgrade

def apply_migrations():
    """Apply all pending migrations"""
    
    app = create_app()
    
    with app.app_context():
        print("Applying migrations...")
        try:
            upgrade()
            print("✅ Migrations applied successfully!")
        except Exception as e:
            print(f"❌ Error applying migrations: {e}")
            return False
    
    return True


if __name__ == '__main__':
    apply_migrations()

