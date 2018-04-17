#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Hapcat database management utilities.
"""

from __future__ import absolute_import, with_statement, print_function

import hapcat.models

from hapcat.models import (
    Tag,
    Location,
)

import sqlalchemy
import sqlalchemy.orm
import alembic.config
import alembic

import json
from pkg_resources import resource_string

def gen_alembic_config(dburl):
    """Generate the alembic run-time config
    """

    config = alembic.config.Config()
    config.set_main_option('script_location', 'hapcat:migrations')
    config.set_main_option('url', dburl)

    return config

def add_test_data(engine, sessionfact):
    """Load the test data into the database.
    """

    testdata = json.loads(
        resource_string('hapcat', 'data/test-suggestions.json').decode()
    )

    session = sessionfact()

    # Load tags.
    for tag in testdata['tags'].values():
        session.add(
            Tag(
                id=tag['id'],
                name=tag['name']
            )
        )

    # Load locations.
    for location in testdata['locations'].values():
        newloc = Location(
            id=location['id'],
            name=location.get('name', None),
            address=location.get('address', None)
        )

        newloc.tags.extend(location.get('tags', []))

        session.add(newloc)

    session.commit()
    session.close()

def initdb(config):
    """Initialize the database if necessary.

    This also takes care of migrations if needed.
    """

    dburl = config.get('database', 'dburl')

    alconfig = gen_alembic_config(dburl)

    engine = sqlalchemy.create_engine(dburl)

    # First, check if the database is initialized.

    firsttime = False

    if engine.dialect.has_table(engine, 'alembic_version'):
        # The database is initialized, try to migrate.

        print('Attempting to migrate database...')

        with engine.begin() as connection:
            alconfig.attributes['connection'] = connection
            alembic.command.upgrade(alconfig, 'head')

    else:
        # The database is empty I suppose, let's create it and stamp it as the
        # head revision.

        print('Creating database...')

        hapcat.models.Base.metadata.create_all(engine)

        firsttime = True

    sessionfact = sqlalchemy.orm.sessionmaker(
        bind=engine
    )

    hapcat.models.Base.metadata.bind = engine

    if firsttime and config.getboolean('database', 'loadtestdata'):
        add_test_data(engine, sessionfact)

    if firsttime:
        with engine.begin() as connection:
            alconfig.attributes['connection'] = connection
            alembic.command.stamp(alconfig, 'head')

    return engine, sessionfact
