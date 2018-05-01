#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Hapcat database management utilities.
"""

from __future__ import absolute_import, with_statement, print_function

import hapcat.models

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
            app.logger.debug(
                'Skipping duplicate tag id=%s, name=%s',
                tag['id'],
                tag['name'],
            )

    # Load locations.
    for location in testdata['locations'].values():
        try:
            with session.begin_nested():
                newloc = None

                if location.get('ephemeral', False):
                    newloc = RawLocation(
                        id=location['id'],
                        address=location['address'],
                    )

                else:
                    newloc = Location(
                        id=location['id'],
                        name=location['name'],
                        address=location['address']
                    )

                    newloc.tags.extend(location['tags'])

                session.add(newloc)
        except IntegrityError:
            app.logger.debug(
                'Skipping duplicate location id=%s, name=%s',
                location['id'],
                location.get('id', '<none>'),
            )

    session.commit()
