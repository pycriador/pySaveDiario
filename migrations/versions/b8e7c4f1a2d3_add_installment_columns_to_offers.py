"""Add installment columns to offers

Revision ID: b8e7c4f1a2d3
Revises: 3746ae2ab69a
Create Date: 2025-03-13

"""
from alembic import op
import sqlalchemy as sa


revision = 'b8e7c4f1a2d3'
down_revision = '3746ae2ab69a'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('offers', sa.Column('installment_count', sa.Integer(), nullable=True))
    op.add_column('offers', sa.Column('installment_value', sa.Numeric(10, 2), nullable=True))
    op.add_column('offers', sa.Column('installment_interest_free', sa.Boolean(), nullable=True))


def downgrade():
    op.drop_column('offers', 'installment_interest_free')
    op.drop_column('offers', 'installment_value')
    op.drop_column('offers', 'installment_count')
