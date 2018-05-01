"""Add RawLocations

Revision ID: d14fd711a3a3
Revises: f008e0185df5
Create Date: 2018-04-30 23:55:21.878340

"""
from alembic import op
import sqlalchemy as sa
import hapcat.types


# revision identifiers, used by Alembic.
revision = 'd14fd711a3a3'
down_revision = 'f008e0185df5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('rawlocation',
    sa.Column('id', hapcat.types.GUID(), nullable=False),
    sa.Column('address', sa.UnicodeText(), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['uuidobject.id'], name=op.f('fk-rawlocation-id-uuidobject-id')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk-rawlocation'))
    )
    op.drop_constraint('fk-location-id-uuidobject-id', 'location', type_='foreignkey')
    op.create_foreign_key(op.f('fk-location-id-rawlocation-id'), 'location', 'rawlocation', ['id'], ['id'])
    op.drop_column('location', 'address')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('location', sa.Column('address', sa.TEXT(), autoincrement=False, nullable=True))
    op.drop_constraint(op.f('fk-location-id-rawlocation-id'), 'location', type_='foreignkey')
    op.create_foreign_key('fk-location-id-uuidobject-id', 'location', 'uuidobject', ['id'], ['id'])
    op.drop_table('rawlocation')
    # ### end Alembic commands ###