#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Hapcat database models.
"""

from __future__ import absolute_import, with_statement, print_function

from hapcat.types import GUID

from hapcat import db

import sqlalchemy.ext.associationproxy
db.association_proxy = sqlalchemy.ext.associationproxy.association_proxy

# Set the constraint naming conventions.

db.Model.metadata.naming_convention = {
    'fk': 'fk-%(table_name)s-%(column_0_name)s-'
        '%(referred_table_name)s-%(referred_column_0_name)s',
    'pk': 'pk-%(table_name)s',
    'ix': 'ix-%(table_name)s-%(column_0_label)s',
    'ck': 'ck-%(table_name)s-%(constraint_name)s',
    'uq': 'uq-%(table_name)s-%(column_0_name)s',
}


class Tag(db.Model):
    __tablename__ = 'tag'

    id = db.Column(GUID, primary_key=True)
    name = db.Column(db.UnicodeText, nullable=False)

class Location(db.Model):
    __tablename__ = 'location'

    id = db.Column(GUID, primary_key=True)
    name = db.Column(db.UnicodeText)
    address = db.Column(db.UnicodeText)

    tags = db.association_proxy(
        'location_tags',
        'tag',
        creator=lambda tag: LocationTag(tag_id=tag)
    )

class LocationTag(db.Model):
    __tablename__ = 'location_tag'

    location_id = db.Column(
        GUID,
        db.ForeignKey('location.id'),
        primary_key=True
    )

    tag_id = db.Column(GUID, db.ForeignKey('tag.id'), primary_key=True)

    location = db.relationship(
        Location,
        backref=db.backref('location_tags', cascade='all, delete-orphan')
    )

    tag = db.relationship('Tag')
