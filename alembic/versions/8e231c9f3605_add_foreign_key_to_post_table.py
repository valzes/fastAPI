"""add foreign key to post table

Revision ID: 8e231c9f3605
Revises: 0f533b057519
Create Date: 2021-12-15 12:00:39.531822

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8e231c9f3605'
down_revision = '0f533b057519'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('fk_posts_owner_id', source_table='posts',
                          referent_table='users', local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")


def downgrade():
    op.drop_constraint('fk_posts_owner_id', 'posts')
    op.drop_column('posts', 'owner_id')
