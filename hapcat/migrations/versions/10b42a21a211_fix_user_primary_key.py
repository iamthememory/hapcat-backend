"""Fix the User primary key

Revision ID: 10b42a21a211
Revises: 2f64ffb0130b
Create Date: 2018-05-01 23:29:56.476908

"""
from alembic import op
import sqlalchemy as sa
import hapcat.types
import sqlalchemy_utils.types


# revision identifiers, used by Alembic.
revision = '10b42a21a211'
down_revision = '2f64ffb0130b'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_constraint('pk-user', 'user')
    op.create_primary_key('pk-user', 'user', ['id'])


def downgrade():
    op.drop_constraint('pk-user', 'user')
    op.create_primary_key('pk-user', 'user', ['username'])
