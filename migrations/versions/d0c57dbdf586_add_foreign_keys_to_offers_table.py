"""Add foreign keys to offers table

Revision ID: d0c57dbdf586
Revises: 70a048e34438
Create Date: 2025-12-03 10:46:39.976110

Note: Columns and FKs (seller_id, category_id, manufacturer_id) are already
added by 70a048e34438. This revision is a no-op to avoid duplicate work and
CircularDependencyError in SQLite batch_alter_table when adding multiple FKs.
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd0c57dbdf586'
down_revision = '70a048e34438'
branch_labels = None
depends_on = None


def upgrade():
    # Already applied in 70a048e34438 (sellers, categories, manufacturers + offers FKs).
    pass


def downgrade():
    # No-op: do not drop columns/FKs here; reverted by 70a048e34438 downgrade.
    pass
