"""add content column

Revision ID: 6014d516d6a0
Revises: eb69c12e0b70
Create Date: 2022-01-07 22:38:54.391448

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.sqltypes import String


# revision identifiers, used by Alembic.
revision = '6014d516d6a0'
down_revision = 'eb69c12e0b70'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))


def downgrade():
    op.drop_column('posts','content')
