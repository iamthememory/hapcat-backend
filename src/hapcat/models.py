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


class Tag(Base):
    __tablename__ = 'tag'

    id = Column(GUID, primary_key=True)
    name = Column(UnicodeText, nullable=False)

class Location(Base):
    __tablename__ = 'location'

    id = Column(GUID, primary_key=True)
    name = Column(UnicodeText)
    address = Column(UnicodeText)

    tags = association_proxy('location_tags', 'tag')

class LocationTag(Base):
    __tablename__ = 'location_tag'
    location_id = Column(GUID, ForeignKey('location.id'), primary_key=True)
    tag_id = Column(GUID, ForeignKey('tag.id'), primary_key=True)

    location = relationship(
        Location,
        backref=backref('location_tags', cascade='all, delete-orphan')
    )

    tag = relationship('Tag')
