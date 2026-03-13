"""Add discount columns to coupons table

Revision ID: c4d5e6f7a8b9
Revises: b8e7c4f1a2d3
Create Date: 2025-03-13

"""
from alembic import op
import sqlalchemy as sa


revision = 'c4d5e6f7a8b9'
down_revision = 'b8e7c4f1a2d3'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('coupons', sa.Column('discount_type', sa.String(20), nullable=True))
    op.add_column('coupons', sa.Column('discount_value', sa.Numeric(10, 2), nullable=True))
    op.add_column('coupons', sa.Column('min_purchase_value', sa.Numeric(10, 2), nullable=True))
    op.add_column('coupons', sa.Column('max_discount_value', sa.Numeric(10, 2), nullable=True))
    # Set default for existing rows (percentage)
    op.execute("UPDATE coupons SET discount_type = 'percentage' WHERE discount_type IS NULL")


def downgrade():
    op.drop_column('coupons', 'max_discount_value')
    op.drop_column('coupons', 'min_purchase_value')
    op.drop_column('coupons', 'discount_value')
    op.drop_column('coupons', 'discount_type')
