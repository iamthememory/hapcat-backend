#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Hapcat database models.
"""

from __future__ import absolute_import, with_statement, print_function

from hapcat.types import GUID

from hapcat import (
    app,
    bcrypt,
    db,
)

import sqlalchemy.ext.associationproxy
db.association_proxy = sqlalchemy.ext.associationproxy.association_proxy

import sqlalchemy.ext.hybrid
db.hybrid_property = sqlalchemy.ext.hybrid.hybrid_property
db.hybrid_method = sqlalchemy.ext.hybrid.hybrid_method

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

class User(db.Model):
    __tablename__ = 'user'

    def __init__(self, username, email, date_of_birth, password):
        self.username = username
        self.email = email
        self.date_of_birth = date_of_birth
        self.password = password

    username = db.Column(
        db.UnicodeText,
        primary_key=True,
    )

    email = db.Column(
        db.UnicodeText,
        nullable=False,
    )

    date_of_birth = db.Column(
        db.Date,
        nullable=False,
    )

    _password = db.Column(
        'password_hash',
        db.Binary(60),
        nullable=False,
    )

    @db.hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, plainpw):
        self._password = bcrypt.generate_password_hash(plainpw)

    @db.hybrid_method
    def is_correct_password(self, plainpw):
        return bcrypt.check_password_hash(self.password, plainpw)
