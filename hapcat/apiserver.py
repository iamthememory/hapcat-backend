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

import hapcat.dbutil

from flask_api.decorators import set_renderers
from flask_api.renderers import JSONRenderer, HTMLRenderer
from flask_api import status

@app.route('/api/v<int:version>/serverinfo/')
def serverinfo(
        version,
    ):
    """Get the server info.

    :query version: The version of the API currently in use

    :>json string server_version: The version of the backend

    :>json list(int) api_versions: The supported API versions

    :statuscode 200: No error

    **Example request**:

    .. http:example:: curl

        GET /api/v0/serverinfo/ HTTP/1.0
        Accept: application/json

    **Example response**:

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        {
            "server_version": "0.0.2.dev10",
            "api_versions": [
                0
            ]
        }
    """

    return {
        'server_version': hapcat.__version__,
        'api_versions': hapcat.__api_versions__,
    }

@app.route('/api/serverinfo/')
def serverinfo_redirect():
    """Redirect to the latest API version serverinfo.

    :statuscode 302: Redirect

    **Example request**:

    .. http:example:: curl

        GET /api/serverinfo/ HTTP/1.1

    **Example response**:

    .. sourcecode:: http

        HTTP/1.0 302 FOUND
        Location: http://localhost:8080/api/v0/serverinfo/

    """

    return flask.redirect('/api/v0/serverinfo/')

@app.route('/api/v<int:version>/tag/<tag>')
def tag(
        version,
        tag,
    ):
    """
    """
    return {}

@app.route('/api/v<int:version>/location/<location>')
def location(
        version,
        location,
    ):
    """
    """
    return {}

@app.route('/api/v<int:version>/event/<event>')
def event(
        version,
        event,
    ):
    """
    """
    return {}


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

@app.route('/reloadtestdata/')
def load_testdata():
    """Load our test data.
    """

    hapcat.dbutil.load_test_data()

    return {'success': 'true'}


@app.route('/api/v<int:version>/registration/', methods=['POST'])
@app.route('/api/v<int:version>/register/', methods=['POST'])
def register(version):
    """Register user.
    """

    data = flask.request.get_json(
        force=True,
    )
    dob = data['date_of_birth']

    newuser = User(
        id=uuid.uuid4(),
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
