"""Add photos and event-photos

Revision ID: a01bf8ab170d
Revises: dd02119e8e12
Create Date: 2018-05-01 03:22:50.100190

"""
from alembic import op
import sqlalchemy as sa
import hapcat.types
import sqlalchemy_utils.types


# revision identifiers, used by Alembic.
revision = 'a01bf8ab170d'
down_revision = 'dd02119e8e12'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('photo',
    sa.Column('id', sqlalchemy_utils.types.uuid.UUIDType, nullable=False),
    sa.Column('photourl', sqlalchemy_utils.types.url.URLType(), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['uuidobject.id'], name=op.f('fk-photo-id-uuidobject-id'), ondelete='cascade'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk-photo')),
    sa.UniqueConstraint('photourl', name=op.f('uq-photo-photourl'))
    )
    op.create_table('event_photo',
    sa.Column('event_id', sqlalchemy_utils.types.uuid.UUIDType, nullable=False),
    sa.Column('photo_id', sqlalchemy_utils.types.uuid.UUIDType, nullable=False),
    sa.ForeignKeyConstraint(['event_id'], ['event.id'], name=op.f('fk-event_photo-event_id-event-id'), ondelete='cascade'),
    sa.ForeignKeyConstraint(['photo_id'], ['photo.id'], name=op.f('fk-event_photo-photo_id-photo-id'), ondelete='cascade'),
    sa.PrimaryKeyConstraint('event_id', 'photo_id', name=op.f('pk-event_photo'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('event_photo')
    op.drop_table('photo')
    # ### end Alembic commands ###