"""Add user table

Revision ID: 789c0115af6c
Revises: 80bdeead8a92
Create Date: 2018-04-18 20:02:04.431193

"""
from alembic import op
import sqlalchemy as sa
import hapcat.types


# revision identifiers, used by Alembic.
revision = '789c0115af6c'
down_revision = '80bdeead8a92'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('username', sa.UnicodeText(), nullable=False),
    sa.Column('email', sa.UnicodeText(), nullable=False),
    sa.Column('date_of_birth', sa.Date(), nullable=False),
    sa.Column('password_hash', sa.Binary(), nullable=False),
    sa.PrimaryKeyConstraint('username', name=op.f('pk-user'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###
