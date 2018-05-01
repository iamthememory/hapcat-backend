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

        GET /api/serverinfo/ HTTP/1.0

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
    """Get the given tag's info.

    :query version: The version of the API currently in use

    :query tag: The UUID of the tag to get info for

    :statuscode 200: Success

    :statuscode 400: Invalid tag ID

    **Example request**:

    .. http:example:: curl

        GET /api/v0/tag/d927d94f-beb8-4295-ac78-5c00e6dc217c HTTP/1.0
        Accept: application/json

    **Example success**:

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        {
            "id": "d927d94f-beb8-4295-ac78-5c00e6dc217c",
            "name": "healthy",
            "type": "tag"
        }

    **Example failure**:

    .. sourcecode:: http

        HTTP/1.0 400 BAD REQUEST
        Content-Type: application/json

        {
            "status": "failure",
            "message": "Invalid tag ID"
        }
    """

    try:
        tagid = uuid.UUID(tag)
        tagobj = db.session.query(Tag).filter_by(id=tagid).first()

        if tagobj:
            return tagobj.serialize()

        else:
            return (
                {
                    'status': 'failure',
                    'message': 'No such tag',
                },
                status.HTTP_400_BAD_REQUEST
            )

    except ValueError:
        return (
            {
                'status': 'failure',
                'message': 'Invalid tag ID',
            },
            status.HTTP_400_BAD_REQUEST
        )

@app.route('/api/v<int:version>/location/<location>')
def location(
        version,
        location,
    ):
    """FIXME: Stub
    """
    return {}

@app.route('/api/v<int:version>/event/<event>')
def event(
        version,
        event,
    ):
    """FIXME: Stub
    """
    return {}


@app.route('/api/v<int:version>/suggestions/')
def suggestions(
        version,
    ):
    """Send our suggestions.

    :query version: The version of the API currently in use

    :>json tags: The tags, by ID.
        See the documentation for
        :http:get:`/api/v(int:version)/tag/(tag)`.

    :>json locations: The locations, by ID.
        See the documentation for
        :http:get:`/api/v(int:version)/location/(location)`.

    :>json events: The events, by ID.
        See the documentation for
        :http:get:`/api/v(int:version)/event/(event)`.

    :>json order: The order of the suggestions

    :statuscode 200: No error

    **Example request**:

    .. http:example:: curl

        GET /api/v0/suggestions/ HTTP/1.0
        Accept: application/json

    **Example response**:

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        {
            "tags": {
                "d927d94f-beb8-4295-ac78-5c00e6dc217c": {
                    "id": "d927d94f-beb8-4295-ac78-5c00e6dc217c",
                    "name": "healthy"
                }
                "64b9eae5-b220-4a57-92f4-c21dc9b19ec5": {
                    "id": "64b9eae5-b220-4a57-92f4-c21dc9b19ec5",
                    "name": "concert"
                },
            },
            "locations": {
                "f8293fe1-d439-4a4d-ac84-5e8290a28c23": {
                    "address": "1075 Risman Dr, Kent, OH 44242",
                    "tags": [
                        "d927d94f-beb8-4295-ac78-5c00e6dc217c",
                    ],
                    "id": "f8293fe1-d439-4a4d-ac84-5e8290a28c23",
                    "name": "Fresco",
                    "photos": [
                        "https://media-cdn.tripadvisor.com/media/photo-s/03/2b/02/a1/fresco-mexican-grill.jpg"
                    ]
                }
                "cbedf9e2-4a1a-44b9-9e3f-6fe870405329": {
                    "address": "175 E Main St, Kent, OH 44240",
                    "ephemeral": true,
                    "id": "cbedf9e2-4a1a-44b9-9e3f-6fe870405329"
                },
            },
            "events": {
                "b0a28a40-b8ad-4131-8c64-071f3fd45bee": {
                    "location": "cbedf9e2-4a1a-44b9-9e3f-6fe870405329",
                    "id": "b0a28a40-b8ad-4131-8c64-071f3fd45bee",
                    "name": "The Accidentals - Concert at the Kent Stage",
                    "photos": [
                        "https://image-ticketfly.imgix.net/00/02/83/80/81-og.jpg"
                    ],
                    "tags": [
                        "64b9eae5-b220-4a57-92f4-c21dc9b19ec5",
                    ]
                }
            },
            "order": [
                {
                    "section": "locations",
                    "id": "f8293fe1-d439-4a4d-ac84-5e8290a28c23"
                },
                {
                    "section": "events",
                    "id": "b0a28a40-b8ad-4131-8c64-071f3fd45bee"
                }
            ]
        }
    """

    sugs = resource_string('hapcat', 'data/test-suggestions.json')
    return json.loads(sugs.decode())

@app.route('/')
def dump_routes():
    """Dump the routes for debugging.

    See `the API docs
    <https://hapcat-backend.readthedocs.io/en/latest/api.html>`_ for details.
    """
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
    """Load our test data for debugging.

    A request to this reloads the test data into the database.
    """

    hapcat.dbutil.load_test_data()

    return {'success': 'true'}


@app.route('/api/v<int:version>/registration/', methods=['POST'])
@app.route('/api/v<int:version>/register/', methods=['POST'])
def register(version):
    """Register the given user.

    :query version: The version of the API currently in use.

    :<json string username: The requested username.

    :<json string email: The user's email address.

    :<json date_of_birth: The user's date of birth.

    :<json string password: The user's password.

    :>json string status: ``success`` or ``failure``.

    :>json string username: The username.

    :>json string message: An optional message on failure.

    :statuscode 200: Success

    :statuscode 409: The username is already taken.

    **Example request**:

    .. http:example:: curl

        POST /api/v0/registration/ HTTP/1.0
        Accept: application/json
        Content-Type: application/json

        {
            "username": "user",
            "password": "password",
            "email": "user@example.com",
            "date_of_birth": {
                "year": 1999,
                "month": 9,
                "day": 9
            }
        }

    **Example success**:

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        {
            "status": "success",
            "username": "user"
        }

    **Example failure**:

    .. sourcecode:: http

        HTTP/1.0 409 CONFLICT
        Content-Type: application/json

        {
            "status": "failure",
            "username": "user",
            "message": "Username already exists"
        }
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
