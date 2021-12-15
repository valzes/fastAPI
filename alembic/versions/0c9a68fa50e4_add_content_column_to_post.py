"""add content column to post

Revision ID: 0c9a68fa50e4
Revises: f3269b3eb79e
Create Date: 2021-12-15 11:38:25.071986

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0c9a68fa50e4'
down_revision = 'f3269b3eb79e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
