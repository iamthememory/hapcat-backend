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

from zxcvbn import zxcvbn

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

    address = db.Column(
        db.UnicodeText,
        nullable=False,
        unique=True,
        index=True,
    )

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


class Votable(UUIDObject):
    __tablename__ = 'votable'

    id = db.Column(
        UUIDType,
        db.ForeignKey('uuidobject.id', ondelete='cascade'),
        primary_key=True
    )

    name = db.Column(
        db.UnicodeText,
        nullable=False
    )

    tags = db.association_proxy(
        'votable_tags',
        'tag',
        creator=lambda tag: VotableTag(tag_id=tag)
    )

    photos = db.association_proxy(
        'votable_photos',
        'photo',
        creator=lambda photo: VotablePhoto(photo_id=photo)
    )

    __mapper_args__ = {
        'polymorphic_identity': 'votable',
    }


class Location(Votable):
    __tablename__ = 'location'

    id = db.Column(
        UUIDType,
        db.ForeignKey('votable.id', ondelete='cascade'),
        primary_key=True
    )

    rawlocation_id = db.Column(
        UUIDType,
        db.ForeignKey('rawlocation.id', ondelete='cascade'),
        nullable=False,
    )

    rawlocation = db.relationship(
        RawLocation,
    )

    __mapper_args__ = {
        'polymorphic_identity': 'location',
    }

    def serialize(self):
        return {
            'id': self.id,
            'address': self.rawlocation.address,
            'name': self.name,
            'ephemeral': False,
            'tags': [tag.id for tag in self.tags],
            'type': 'location',
            'photos': [str(photo.photourl) for photo in self.photos],
        }


class VotableTag(db.Model):
    __tablename__ = 'votable_tag'

    votable_id = db.Column(
        UUIDType,
        db.ForeignKey('votable.id', ondelete='cascade'),
        primary_key=True,
    )

    tag_id = db.Column(
        UUIDType,
        db.ForeignKey('tag.id', ondelete='cascade'),
        primary_key=True,
    )

    votable = db.relationship(
        Votable,
        backref=db.backref('votable_tags', cascade='all, delete-orphan'),
    )

    tag = db.relationship(Tag)


class Event(Votable):
    __tablename__ = 'event'

    id = db.Column(
        UUIDType,
        db.ForeignKey('votable.id', ondelete='cascade'),
        primary_key=True,
    )

    rawlocation_id = db.Column(
        UUIDType,
        db.ForeignKey('rawlocation.id', ondelete='cascade'),
        nullable=False,
    )

    rawlocation = db.relationship(
        'RawLocation',
        foreign_keys=[rawlocation_id],
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

    votables = db.association_proxy(
        'votable_photos',
        'votable',
        creator=lambda votable: VotablePhoto(votable_id=votable),
    )

    __mapper_args__ = {
        'polymorphic_identity': 'photo'
    }


class VotablePhoto(db.Model):
    __tablename__ = 'votable_photo'

    votable_id = db.Column(
        UUIDType,
        db.ForeignKey('votable.id', ondelete='cascade'),
        primary_key=True,
    )

    votable = db.relationship(
        Votable,
        backref=db.backref('votable_photos', cascade='all, delete-orphan'),
    )

    photo_id = db.Column(
        UUIDType,
        db.ForeignKey('photo.id', ondelete='cascade'),
        primary_key=True,
    )

    photo = db.relationship(
        Photo,
        backref=db.backref('votable_photos', cascade='all, delete-orphan'),
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

    votes = db.association_proxy(
        'user_votes',
        'vote',
        creator=lambda votable: Vote(votable_id=votable)
    )

    __mapper_args__ = {
        'polymorphic_identity': 'user'
    }

    @staticmethod
    def checkpwstrength(
        password,
        username,
        email,
        minscore=3,
    ):
        """Check the user's password strength.
        """

        results = zxcvbn(password, user_inputs=[username, email])

        if results['score'] >= minscore:
            return (True, results['feedback'])
        else:
            return (False, results['feedback'])


class Vote(db.Model):
    __tablename__ = 'vote'

    votable_id = db.Column(
        UUIDType,
        db.ForeignKey('votable.id', ondelete='cascade'),
        primary_key=True,
    )

    user_id = db.Column(
        UUIDType,
        db.ForeignKey('user.id', ondelete='cascade'),
        primary_key=True,
    )

    numvotes = db.Column(
        db.Integer,
        default=0,
        nullable=False,
    )

    votable = db.relationship(
        Votable,
    )

    user = db.relationship(
        User,
        backref=db.backref('user_votes', cascade='all, delete-orphan'),
    )


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
