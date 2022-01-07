"""create post table

Revision ID: eb69c12e0b70
Revises:
Create Date: 2022-01-07 22:29:10.181084

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eb69c12e0b70'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
    sa.Column('title', sa.String(), nullable=False))


def downgrade():
    op.op.drop_table('posts')
