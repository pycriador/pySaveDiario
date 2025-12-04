#!/usr/bin/env python
"""
Add max_discount_value column to coupons table

This script adds the max_discount_value field to store the maximum
discount limit for percentage-based coupons.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db

def add_max_discount_value_column():
    """Add max_discount_value column to coupons table"""
    app = create_app()
    
    with app.app_context():
        try:
            # Check if column already exists
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('coupons')]
            
            if 'max_discount_value' in columns:
                print("✅ Column 'max_discount_value' already exists in 'coupons' table.")
                return
            
            # Add column
            with db.engine.connect() as conn:
                conn.execute(db.text(
                    "ALTER TABLE coupons ADD COLUMN max_discount_value NUMERIC(10, 2)"
                ))
                conn.commit()
            
            print("✅ Successfully added 'max_discount_value' column to 'coupons' table!")
            print("\n📝 Usage:")
            print("   - For percentage discounts: Set max discount limit (e.g., 70 for R$ 70 max)")
            print("   - For fixed discounts: Leave empty (not used)")
            print("\n💡 Example:")
            print("   Coupon: 10% discount, max R$ 70")
            print("   - Product R$ 500 → 10% = R$ 50 → Final: R$ 450")
            print("   - Product R$ 1000 → 10% = R$ 100, limited to R$ 70 → Final: R$ 930")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            raise

if __name__ == "__main__":
    add_max_discount_value_column()

