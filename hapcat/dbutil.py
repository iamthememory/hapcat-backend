#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Hapcat database management utilities.
"""

from __future__ import absolute_import, with_statement, print_function

import hapcat.models
import uuid

from hapcat.models import *

import sqlalchemy
import sqlalchemy.orm
import alembic.config
import alembic
from hapcat import (
    app,
    db,
)

from sqlalchemy.exc import (
    IntegrityError,
)

import json
from pkg_resources import resource_string

def load_test_data():
    """Load the test data into the database.
    """

    session = db.session

    testdata = json.loads(
        resource_string('hapcat', 'data/test-suggestions.json').decode()
    )

    app.logger.info('Loading test data')

    # Load tags.
    for tag in testdata['tags'].values():
        try:
            with session.begin_nested():
                session.add(
                    Tag(
                        id=tag['id'],
                        name=tag['name']
                    )
                )
        except IntegrityError:
            pass

    # Load locations.
    for location in testdata['locations'].values():
        try:
            with session.begin_nested():
                if location.get('ephemeral', False):
                    newloc = RawLocation(
                        id=location['id'],
                        address=location['address'],
                    )

                    session.add(newloc)

                else:
                    rawloc = RawLocation(
                        id=uuid.uuid4(),
                        address=location['address'],
                    )

                    newloc = Location(
                        id=location['id'],
                        name=location['name'],
                        rawlocation=rawloc
                    )

                    newphotos = [
                        Photo(
                            id=uuid.uuid4(),
                            photourl=photo,
                        )
                        for photo in location['photos']
                    ]

                    session.add_all(newphotos)

                    newloc.photos.extend([p.id for p in newphotos])

                    newloc.tags.extend(location['tags'])

                    session.add(rawloc)
                    session.add(newloc)
        except IntegrityError:
            pass

    # Load events.
    for event in testdata['events'].values():
        try:
            with session.begin_nested():
                newevent = Event(
                    id=event['id'],
                    rawlocation_id=event['location'],
                    name=event['name'],
                )

                newevent.tags.extend(event['tags'])

                newphotos = [
                    Photo(
                        id=uuid.uuid4(),
                        photourl=photo,
                    )
                    for photo in event['photos']
                ]

                session.add_all(newphotos)

                newevent.photos.extend([p.id for p in newphotos])
                session.add(newevent)
        except IntegrityError:
            pass

    session.commit()
