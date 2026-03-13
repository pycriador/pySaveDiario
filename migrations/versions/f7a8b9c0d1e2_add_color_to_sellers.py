"""Add color column to sellers table

Revision ID: f7a8b9c0d1e2
Revises: e6f7a8b9c0d1
Create Date: 2025-03-13

"""
from alembic import op
import sqlalchemy as sa


revision = 'f7a8b9c0d1e2'
down_revision = 'e6f7a8b9c0d1'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'sellers',
        sa.Column('color', sa.String(255), nullable=True),
    )


def downgrade():
    op.drop_column('sellers', 'color')
