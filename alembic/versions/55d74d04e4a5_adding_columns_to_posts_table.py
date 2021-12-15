"""adding columns to posts table

Revision ID: 55d74d04e4a5
Revises: 8e231c9f3605
Create Date: 2021-12-15 12:04:21.428604

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '55d74d04e4a5'
down_revision = '8e231c9f3605'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published', sa.Boolean(),
                  nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                  server_default=sa.text('NOW()'), nullable=False))


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
