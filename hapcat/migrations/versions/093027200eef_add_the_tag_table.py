"""Add the tag table

Revision ID: 093027200eef
Revises:
Create Date: 2018-04-06 00:16:23.408746

"""
from alembic import op
import sqlalchemy as sa
import hapcat.types


# revision identifiers, used by Alembic.
revision = '093027200eef'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'tag',
        sa.Column('id', hapcat.types.GUID()),
        sa.Column('name', sa.UnicodeText, nullable=False),
        sa.PrimaryKeyConstraint('id', name=op.f('pk-tag'))
    )


def downgrade():
    op.drop_table('tag')
