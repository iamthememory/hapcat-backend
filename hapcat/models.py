#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Hapcat database models.
"""

from __future__ import absolute_import, with_statement, print_function

from sqlalchemy_utils.types import (
    EmailType,
    PasswordType,
    URLType,
    UUIDType,
)

from hapcat import (
    app,
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


class UUIDObject(db.Model):
    __tablename__ = 'uuidobject'

    id = db.Column(UUIDType, primary_key=True)
    type = db.Column(db.String(32))

    __mapper_args__ = {
        'polymorphic_identity': 'uuidobject',
        'polymorphic_on': type
    }


class Tag(UUIDObject):
    __tablename__ = 'tag'

    id = db.Column(
        UUIDType,
        db.ForeignKey('uuidobject.id', ondelete='cascade'),
        primary_key=True
    )

    name = db.Column(db.UnicodeText, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'tag'
    }

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': 'tag',
        }


class RawLocation(UUIDObject):
    __tablename__ = 'rawlocation'

    id = db.Column(
        UUIDType,
        db.ForeignKey('uuidobject.id', ondelete='cascade'),
        primary_key=True
    )

    address = db.Column(db.UnicodeText)

    __mapper_args__ = {
        'polymorphic_identity': 'rawlocation',
    }

    def serialize(self):
        return {
            'id': self.id,
            'address': self.address,
            'ephemeral': True,
            'type': 'rawlocation',
        }


class Location(RawLocation):
    __tablename__ = 'location'

    id = db.Column(
        UUIDType,
        db.ForeignKey('rawlocation.id', ondelete='cascade'),
        primary_key=True
    )

    name = db.Column(db.UnicodeText, nullable=False)

    tags = db.association_proxy(
        'location_tags',
        'tag',
        creator=lambda tag: LocationTag(tag_id=tag)
    )

    photos = db.association_proxy(
        'location_photos',
        'photo',
        creator=lambda photo: LocationPhoto(photo_id=photo)
    )

    __mapper_args__ = {
        'polymorphic_identity': 'location',
    }

    def serialize(self):
        return {
            'id': self.id,
            'address': self.address,
            'name': self.name,
            'ephemeral': False,
            'tags': [tag.id for tag in self.tags],
            'type': 'location',
            'photos': [str(photo.photourl) for photo in self.photos],
        }


class LocationTag(db.Model):
    __tablename__ = 'location_tag'

    location_id = db.Column(
        UUIDType,
        db.ForeignKey('location.id', ondelete='cascade'),
        primary_key=True
    )

    tag_id = db.Column(
        UUIDType,
        db.ForeignKey('tag.id', ondelete='cascade'),
        primary_key=True
    )

    location = db.relationship(
        Location,
        backref=db.backref('location_tags', cascade='all, delete-orphan')
    )

    tag = db.relationship('Tag')


class Event(UUIDObject):
    __tablename__ = 'event'

    id = db.Column(
        UUIDType,
        db.ForeignKey('uuidobject.id', ondelete='cascade'),
        primary_key=True
    )

    name = db.Column(
        db.UnicodeText,
        nullable=False
    )

    rawlocation_id = db.Column(
        UUIDType,
        db.ForeignKey('rawlocation.id', ondelete='cascade'),
        nullable=False
    )

    rawlocation = db.relationship(
        'RawLocation',
        foreign_keys=[rawlocation_id],
    )

    tags = db.association_proxy(
        'event_tags',
        'tag',
        creator=lambda tag: EventTag(tag_id=tag)
    )

    photos = db.association_proxy(
        'event_photos',
        'photo',
        creator=lambda photo: EventPhoto(photo_id=photo)
    )

    __mapper_args__ = {
        'polymorphic_identity': 'event',
    }

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'location': self.rawlocation_id,
            'tags': [tag.id for tag in self.tags],
            'type': 'event',
            'photos': [str(photo.photourl) for photo in self.photos],
        }


class EventTag(db.Model):
    __tablename__ = 'event_tag'

    event_id = db.Column(
        UUIDType,
        db.ForeignKey('event.id', ondelete='cascade'),
        primary_key=True
    )

    tag_id = db.Column(
        UUIDType,
        db.ForeignKey('tag.id', ondelete='cascade'),
        primary_key=True
    )

    event = db.relationship(
        Event,
        backref=db.backref('event_tags', cascade='all, delete-orphan')
    )

    tag = db.relationship('Tag')


class Photo(UUIDObject):
    __tablename__ = 'photo'

    id = db.Column(
        UUIDType,
        db.ForeignKey('uuidobject.id', ondelete='cascade'),
        primary_key=True,
    )

    photourl = db.Column(
        URLType,
        nullable=False,
        unique=True,
    )

    events = db.association_proxy(
        'event_photos',
        'event',
        creator=lambda event: EventPhoto(event_id=event),
    )

    locations = db.association_proxy(
        'location_photos',
        'location',
        creator=lambda location: LocationPhoto(location_id=location),
    )

    __mapper_args__ = {
        'polymorphic_identity': 'photo'
    }


class EventPhoto(db.Model):
    __tablename__ = 'event_photo'

    event_id = db.Column(
        UUIDType,
        db.ForeignKey('event.id', ondelete='cascade'),
        primary_key=True,
    )

    photo_id = db.Column(
        UUIDType,
        db.ForeignKey('photo.id', ondelete='cascade'),
        primary_key=True,
    )

    event = db.relationship(
        Event,
        backref=db.backref('event_photos', cascade='all, delete-orphan'),
    )

    photo = db.relationship(
        Photo,
        backref=db.backref('event_photos', cascade='all, delete-orphan'),
    )


class LocationPhoto(db.Model):
    __tablename__ = 'location_photo'

    location_id = db.Column(
        UUIDType,
        db.ForeignKey('location.id', ondelete='cascade'),
        primary_key=True,
    )

    photo_id = db.Column(
        UUIDType,
        db.ForeignKey('photo.id', ondelete='cascade'),
        primary_key=True,
    )

    location = db.relationship(
        Location,
        backref=db.backref('location_photos', cascade='all, delete-orphan'),
    )

    photo = db.relationship(
        Photo,
        backref=db.backref('location_photos', cascade='all, delete-orphan'),
    )


class User(UUIDObject):
    __tablename__ = 'user'

    def __init__(self, id, username, email, date_of_birth, password):
        self.id = id
        self.username = username
        self.email = email
        self.date_of_birth = date_of_birth
        self.password = password

    id = db.Column(
        UUIDType,
        db.ForeignKey('uuidobject.id', ondelete='cascade'),
        primary_key=True
    )

    username = db.Column(
        db.UnicodeText,
        nullable=False,
        index=True,
        unique=True,
    )

    email = db.Column(
        EmailType,
        nullable=False,
    )

    date_of_birth = db.Column(
        db.Date,
        nullable=False,
    )

    password = db.Column(
        PasswordType(
            schemes=[
                'argon2',
                'bcrypt',
            ],
            default='argon2',
            deprecated=['auto'],
        ),
        nullable=False,
        unique=False,
    )

    __mapper_args__ = {
        'polymorphic_identity': 'user'
    }


class Secret(db.Model):
    __tablename__ = 'secret'

    id = db.Column(
        db.Unicode,
        primary_key=True,
    )

    payload = db.Column(
        db.LargeBinary,
        nullable=False,
    )
