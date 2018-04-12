#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Hapcat database models.
"""

from __future__ import absolute_import, with_statement, print_function

from hapcat.types import GUID

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy

from sqlalchemy.orm import (
    backref,
    relationship,
)

from sqlalchemy.schema import (
    Column,
    Table,
    ForeignKey,
)

from sqlalchemy.types import (
    UnicodeText,
    Integer,
)


Base = declarative_base()

# Set the constraint naming conventions.

Base.metadata.naming_convention = {
    'fk': 'fk-%(table_name)s-%(column_0_name)s-'
        '%(referred_table_name)s-%(referred_column_0_name)s',
    'pk': 'pk-%(table_name)s',
    'ix': 'ix-%(table_name)s-%(column_0_label)s',
    'ck': 'ck-%(table_name)s-%(constraint_name)s',
    'uq': 'uq-%(table_name)s-%(column_0_name)s',
}


class Tag(Base):
    __tablename__ = 'tag'

    id = Column(GUID, primary_key=True)
    name = Column(UnicodeText, nullable=False)

class Location(Base):
    __tablename__ = 'location'

    id = Column(GUID, primary_key=True)
    name = Column(UnicodeText)
    address = Column(UnicodeText)

    tags = association_proxy(
        'location_tags',
        'tag',
        creator=lambda tag: LocationTag(tag_id=tag)
    )

class LocationTag(Base):
    __tablename__ = 'location_tag'
    location_id = Column(GUID, ForeignKey('location.id'), primary_key=True)
    tag_id = Column(GUID, ForeignKey('tag.id'), primary_key=True)

    location = relationship(
        Location,
        backref=backref('location_tags', cascade='all, delete-orphan')
    )

    tag = relationship('Tag')
