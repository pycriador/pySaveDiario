"""Add color column to social_network_configs

Revision ID: e6f7a8b9c0d1
Revises: d5e6f7a8b9c0
Create Date: 2025-03-13

"""
from alembic import op
import sqlalchemy as sa


revision = 'e6f7a8b9c0d1'
down_revision = 'd5e6f7a8b9c0'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'social_network_configs',
        sa.Column('color', sa.String(20), nullable=True),
    )


def downgrade():
    op.drop_column('social_network_configs', 'color')
