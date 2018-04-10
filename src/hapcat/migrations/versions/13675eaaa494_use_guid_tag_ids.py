"""Use GUID tag IDs

Revision ID: 13675eaaa494
Revises: 093027200eef
Create Date: 2018-04-06 00:18:25.455926

"""
from alembic import op
import sqlalchemy as sa
import hapcat.types


# revision identifiers, used by Alembic.
revision = '13675eaaa494'
down_revision = '093027200eef'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('tag', 'id',
               existing_type=sa.INTEGER,
               type_=hapcat.types.GUID)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('tag', 'id',
               existing_type=hapcat.types.GUID,
               type_=sa.INTEGER)
    # ### end Alembic commands ###
