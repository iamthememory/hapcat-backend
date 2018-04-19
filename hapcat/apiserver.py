#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Hapcat API server module.
"""

from __future__ import absolute_import

from pkg_resources import resource_string

import hapcat

from hapcat import (
    app,
    db,
)

import datetime

from flask import (
    json,
    request,
)

import uuid
import flask

from sqlalchemy.exc import (
    IntegrityError,
)

from hapcat.models import *

from flask_api.decorators import set_renderers
from flask_api.renderers import JSONRenderer, HTMLRenderer
from flask_api import status

@app.route('/api/v<int:version>/serverinfo/')
def serverinfo(version):
    """Send the server info.
    """

    return {
        'server_version': hapcat.__version__,
        'api_versions': hapcat.__api_versions__,
    }

@app.route('/api/serverinfo/')
def serverinfo_redirect():
    """Redirect to the latest API version serverinfo.
    """

    return flask.redirect('/api/v0/serverinfo/')


@app.route('/api/v<int:version>/suggestions/')
def suggestions(version):
    """Send our suggestions.

    FIXME: Don't use test data.
    """

    sugs = resource_string('hapcat', 'data/test-suggestions.json')
    return json.loads(sugs.decode())

@app.route('/')
def dump_routes():
    rules = {}

    for rule in app.url_map.iter_rules():
        rules[rule.rule] = {
            'rule': rule.rule,
            'endpoint': rule.endpoint,
            'methods': [m for m in rule.methods],
        }

    return rules

@app.route('/api/v<int:version>/registration/', methods=['POST'])
def register(version):
    """Register user.
    """

    data = flask.request.get_json(
        force=True,
    )
    dob = data['date_of_birth']

    newuser = User(
        username=data['username'],
        email=data['email'],
        date_of_birth=datetime.date(
            year=dob['year'],
            month=dob['month'],
            day=dob['day'],
        ),
        password=data['password'],
    )

    try:
        db.session.add(newuser)
        db.session.commit()

        app.logger.info(
            'Created user %s for %s',
            newuser.username,
            newuser.email,
        )

        return {
            'status': 'success',
            'username': newuser.username,
        }

    except sqlalchemy.exc.IntegrityError as e:

        app.logger.info(
            'Failed to create duplicate user %s for %s',
            newuser.username,
            newuser.email,
        )

        return ({
            'status': 'failure',
            'username': newuser.username,
            'message': 'Username already exists',
        }, status.HTTP_409_CONFLICT)
