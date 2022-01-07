"""add foreign key to post tbl

Revision ID: 129396b1de45
Revises: dd953a5f6e4d
Create Date: 2022-01-07 22:58:29.018131

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '129396b1de45'
down_revision = 'dd953a5f6e4d'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users", local_cols=[
                          'owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
