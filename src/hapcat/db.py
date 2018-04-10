#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Hapcat database management utilities.
"""

from __future__ import absolute_import, with_statement, print_function

import hapcat.models
import sqlalchemy
import sqlalchemy.orm
import alembic.config
import alembic

def gen_alembic_config(dburl):
    """Generate the alembic run-time config
    """

    config = alembic.config.Config()
    config.set_main_option('script_location', 'hapcat:migrations')
    config.set_main_option('url', dburl)

    return config

def initdb(dburl):
    """Initialize the database if necessary.

    This also takes care of migrations if needed.
    """

    alconfig = gen_alembic_config(dburl)

    engine = sqlalchemy.create_engine(dburl)

    # First, check if the database is initialized.

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

        with engine.begin() as connection:
            alconfig.attributes['connection'] = connection
            alembic.command.stamp(alconfig, 'head')

    sessionfact = sqlalchemy.orm.sessionmaker(
        bind=engine
    )

    hapcat.models.Base.metadata.bind = engine

    return engine, sessionfact
