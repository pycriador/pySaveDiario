"""Add user profile columns (phone, address, website, social) to users table

Revision ID: d5e6f7a8b9c0
Revises: c4d5e6f7a8b9
Create Date: 2025-03-13

"""
from alembic import op
import sqlalchemy as sa


revision = 'd5e6f7a8b9c0'
down_revision = 'c4d5e6f7a8b9'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('phone', sa.String(20), nullable=True))
    op.add_column('users', sa.Column('address', sa.String(255), nullable=True))
    op.add_column('users', sa.Column('website', sa.String(255), nullable=True))
    op.add_column('users', sa.Column('instagram', sa.String(255), nullable=True))
    op.add_column('users', sa.Column('facebook', sa.String(255), nullable=True))
    op.add_column('users', sa.Column('twitter', sa.String(255), nullable=True))
    op.add_column('users', sa.Column('linkedin', sa.String(255), nullable=True))
    op.add_column('users', sa.Column('youtube', sa.String(255), nullable=True))
    op.add_column('users', sa.Column('tiktok', sa.String(255), nullable=True))


def downgrade():
    op.drop_column('users', 'tiktok')
    op.drop_column('users', 'youtube')
    op.drop_column('users', 'linkedin')
    op.drop_column('users', 'twitter')
    op.drop_column('users', 'facebook')
    op.drop_column('users', 'instagram')
    op.drop_column('users', 'website')
    op.drop_column('users', 'address')
    op.drop_column('users', 'phone')
