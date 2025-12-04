#!/usr/bin/env python3
"""
Add color column to sellers table and set default colors
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import Seller
from sqlalchemy import text

def add_color_to_sellers():
    """Add color column to sellers table"""
    app = create_app()
    
    with app.app_context():
        try:
            # Check if column already exists
            result = db.session.execute(text("PRAGMA table_info(sellers)"))
            columns = [row[1] for row in result.fetchall()]
            
            if 'color' in columns:
                print("✅ Column 'color' already exists in sellers table")
            else:
                # Add column
                db.session.execute(text("ALTER TABLE sellers ADD COLUMN color VARCHAR(255) DEFAULT '#6b7280'"))
                db.session.commit()
                print("✅ Added 'color' column to sellers table")
            
            # Update default colors for known sellers
            color_mappings = {
                'mercado livre': '#FFE600',
                'shopee': '#EE4D2D',
                'amazon': '#FF9900',
                'magazine luiza': '#DC143C',
                'aliexpress': '#E62129',
                'kabum': '#003DA5',
                'casas bahia': '#0070C0',
                'extra': '#00A859',
            }
            
            for seller_name, color in color_mappings.items():
                seller = Seller.query.filter(Seller.name.ilike(seller_name)).first()
                if seller:
                    seller.color = color
                    print(f"✅ Set color {color} for {seller.name}")
            
            db.session.commit()
            print("\n✅ Migration completed successfully!")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error during migration: {str(e)}")
            raise

if __name__ == "__main__":
    add_color_to_sellers()

