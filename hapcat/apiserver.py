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
    jwt,
)

import datetime

from flask import (
    json,
    request,
)

from flask_jwt import (
    current_identity,
    jwt_required,
)

import uuid
import flask

from sqlalchemy.exc import (
    IntegrityError,
)

import random

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

    :>json UUID id: The tag ID

    :>json string name: The tag name

    :>json string type: ``tag``

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
    """Get the given location's info.

    :query version: The version of the API currently in use

    :query location: The UUID of the location to get info for

    :statuscode 200: Success

    :statuscode 400: Invalid location ID

    :>json uuid id: The location ID.

    :>json string address: The location address.

    :>json boolean ephemeral: If true, this location is just an address for
        events.

    :>json string name: The location name if not ephemeral.

    :>json tags: The tag IDs for this location if not ephemeral.

    :>json string type: ``rawlocation`` or ``location``.

    **Example request**:

    .. http:example:: curl

        GET /api/v0/location/a25a1b9a-2f5a-4c76-b19f-eb970d2c7049 HTTP/1.0
        Accept: application/json

    **Example success, normal location**:

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        {
            "id": "a25a1b9a-2f5a-4c76-b19f-eb970d2c7049",
            "address": "1444 E Main St, Kent, OH 44240",
            "name": "Hungry Howie's Pizza",
            "ephemeral": false,
            "tags": [
                "17b20e68-8cde-4bc3-91a2-f5926a3e2b0f",
                "0e858a8b-cd18-4617-8a94-2a8bab4945a9",
                "d6f2989d-d5c0-477d-a8a4-d22e47087ab2"
            ]
        }

    **Example success, raw/ephemeral location**:

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        {
            "id": "cbedf9e2-4a1a-44b9-9e3f-6fe870405329",
            "address": "175 E Main St, Kent, OH 44240",
            "ephemeral": true
        }

    **Example failure**:

    .. sourcecode:: http

        HTTP/1.0 400 BAD REQUEST
        Content-Type: application/json

        {
            "status": "failure",
            "message": "Invalid location ID"
        }
    """

    try:
        locid = uuid.UUID(location)
        locobj = db.session.query(RawLocation).filter_by(id=locid).first()

        if locobj:
            return locobj.serialize()

        else:
            return (
                {
                    'status': 'failure',
                    'message': 'No such location',
                },
                status.HTTP_400_BAD_REQUEST
            )

    except ValueError:
        return (
            {
                'status': 'failure',
                'message': 'Invalid location ID',
            },
            status.HTTP_400_BAD_REQUEST
        )

@app.route('/api/v<int:version>/event/<event>')
def event(
        version,
        event,
    ):
    """Get the given event's info.

    :query version: The version of the API currently in use

    :query event: The UUID of the event to get info for

    :statuscode 200: Success

    :statuscode 400: Invalid event ID

    :>json UUID id: The event ID

    :>json string name: The tag name

    :>json UUID location: The raw location this event takes place at

    :>json string type: ``event``

    :>json tags: The tag IDs for this event

    **Example request**:

    .. http:example:: curl

        GET /api/v0/event/b0a28a40-b8ad-4131-8c64-071f3fd45bee HTTP/1.0
        Accept: application/json

    **Example success**:

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        {
            "id": "b0a28a40-b8ad-4131-8c64-071f3fd45bee",
            "name": "The Accidentals - Concert at the Kent Stage",
            "location": "cbedf9e2-4a1a-44b9-9e3f-6fe870405329",
            "tags": [
                "64b9eae5-b220-4a57-92f4-c21dc9b19ec5",
                "71f450ef-b344-45f3-9b60-0dbda7fce2f0",
                "f8ddde82-331e-43c2-a2fd-985c5eb8fe52"
            ],
            "type": "event"
        }

    **Example failure**:

    .. sourcecode:: http

        HTTP/1.0 400 BAD REQUEST
        Content-Type: application/json

        {
            "status": "failure",
            "message": "Invalid event ID"
        }
    """

    try:
        eventid = uuid.UUID(event)
        eventobj = db.session.query(Event).filter_by(id=eventid).first()

        if eventobj:
            return eventobj.serialize()

        else:
            return (
                {
                    'status': 'failure',
                    'message': 'No such event',
                },
                status.HTTP_400_BAD_REQUEST
            )

    except ValueError:
        return (
            {
                'status': 'failure',
                'message': 'Invalid event ID',
            },
            status.HTTP_400_BAD_REQUEST
        )


@app.route('/api/v<int:version>/vote/<votable>/')
@jwt_required()
def vote(
        version,
        votable,
    ):
    """Vote for an event or location.

    :reqheader Authorization: The JWT authorization token for the user from
        :http:post:`/api/v(int:version)/auth/`.

    :query version: The version of the API currently in use.

    :query votable: The UUID of the event or location to vote for.

    :>json boolean success: ``True`` or ``False``.

    :>json string message: The failure reason if ``False``.

    :>json string votable: The UUID of the event or location voted for.

    :>json string user_id: The UUID of the user.

    :>json string username: The username of the user.

    :>json int numvotes: The total number of votes of this user for this event
        or location.

    :statuscode 200: Success.

    :statuscode 400: Invalid votable ID or user.

    :statuscode 401: Invalid authorization token.

    **Example request**:

    .. http:example:: curl

        GET /api/v0/vote/c43e3c6a-64ad-4cc8-94cd-65d1c8e4ada6/ HTTP/1.0
        Accept: application/json
        Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbG...0UHGO-U0R4PTQ

    **Example success**:

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        {
            "success": true,
            "votable": "c43e3c6a-64ad-4cc8-94cd-65d1c8e4ada6",
            "user_id": "e7d45044-d500-451a-825f-cbff616030f2",
            "username": "user",
            "numvotes": 11
        }

    **Example failure**:

    .. sourcecode:: http

        HTTP/1.0 400 BAD REQUEST
        Content-Type: application/json

        {
            "success": false,
            "message": "No such votable",
            "votable": "c43e3c6a-64ad-4cc8-94cd-65d1c8e4adaf",
            "user_id": "e7d45044-d500-451a-825f-cbff616030f2",
            "username": "user"
        }
    """

    user = db.session.query(User).filter(
        User.id == current_identity.id
    ).scalar()

    if user is None:
        return (
            {
                'success': False,
                'message': 'No such user',
                'votable': votable,
                'user_id': current_identity.id,
            },
            status.HTTP_400_BAD_REQUEST
        )

    try:
        uuid.UUID(votable)
    except ValueError:
        return (
            {
                'success': False,
                'message': 'Invalid UUID',
                'votable': votable,
                'user_id': user.id,
                'username': user.username,
            },
            status.HTTP_400_BAD_REQUEST
        )

    votableobj = db.session.query(Votable).filter(
        Votable.id == votable
    ).scalar()

    if votableobj is None:
        return (
            {
                'success': False,
                'message': 'No such votable',
                'votable': votable,
                'user_id': user.id,
                'username': user.username,
            },
            status.HTTP_400_BAD_REQUEST
        )

    vote = db.session.query(Vote).filter(
        Vote.votable_id == votable and
        Vote.user_id == current_identity.id
    ).scalar()

    if vote is None:
        vote = Vote(
            votable_id=votable,
            user_id=current_identity.id,
            numvotes=0,
        )

    vote.numvotes += 1

    db.session.add(vote)
    db.session.commit()

    return {
        'success': True,
        'votable': votable,
        'user_id': user.id,
        'username': user.username,
        'numvotes': vote.numvotes,
    }


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

    # Retrieve a few events and locations.

    maxlocs = 5
    maxevents = 5

    tags = set()

    # Retrieve some locations.

    locs = db.session.query(Location).limit(maxlocs).all()
    slocs = {}

    for loc in locs:
        tags.update(loc.tags)
        slocs[str(loc.id)] = loc.serialize()

    # Retrieve some events.

    events = db.session.query(Event).limit(maxevents).all()
    sevents = {}
    eventlocs = {}

    for event in events:
        tags.update(event.tags)
        sevents[str(event.id)] = event.serialize()
        eventlocs[str(event.rawlocation.id)] = event.rawlocation.serialize()

    # Retrieve our tags.

    stags = {str(tag.id): tag.serialize() for tag in tags}

    # Generate our order.

    raworder = list(slocs.values()) + list(sevents.values())
    random.shuffle(raworder)

    order = [
        {
            'section': 'locations' if x['type'] == 'location' else 'events',
            'id': x['id'],
        }
        for x in raworder
    ]

    # Add in our raw locations
    slocs.update(eventlocs)

    return {
        'locations': slocs,
        'events': sevents,
        'tags': stags,
        'order': order,
    }


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


@app.route('/debug/reloadtestdata/')
def load_testdata():
    """Load our test data for debugging.

    A request to this reloads the test data into the database.
    """

    hapcat.dbutil.load_test_data()

    return {'success': 'true'}


@app.route('/debug/dropalldata/')
def drop_data():
    """Drop all data.

    A request to this drops all data in the database.
    """

    # This should cascade to delete everything.
    db.session.query(UUIDObject).delete()
    db.session.commit()

    return {'success': 0}


@app.route('/debug/protectedtest/')
@jwt_required()
def protect():
    """Test authorization.

    :reqheader Authorization: The JWT authorization token for the user from
        :http:post:`/api/v(int:version)/auth/`.

    :>json string id: The user's UUID.

    :>json string username: The user's username.

    :statuscode 200: Success.

    :statuscode 401: Invalid authorization token.

    **Example request**:

    .. http:example:: curl

        GET /debug/protectedtest/ HTTP/1.0
        Accept: application/json
        Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbG...0UHGO-U0R4PTQ

    **Example success**:

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        {
            "id": "4cfab2e4-b38f-435f-b9b1-aa8eb8172dcf",
            "username": "user"
        }

    **Example failure**:

    .. sourcecode:: http

        HTTP/1.0 401 UNAUTHORIZED
        Content-Type: application/json
        WWW-Authenticate: JWT realm="Login Required"

        {
            "description": "Request does not contain an access token",
            "error": "Authorization Required",
            "status_code": 401
        }
    """

    return {
        'id': current_identity.id,
        'username': current_identity.username,
    }


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

    :statuscode 400: Insufficient password strength.

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

    **Example failures**:

    .. sourcecode:: http

        HTTP/1.0 409 CONFLICT
        Content-Type: application/json

        {
            "status": "failure",
            "username": "user",
            "message": "Username already exists"
        }

    .. sourcecode:: http

        HTTP/1.0 400 BAD REQUEST
        Content-Type: application/json

        {
            "status": "failure",
            "username": "user",
            "message": "Insufficiently secure password",
            "details": {
                "warning": "This is a top-10 common password.",
                "suggestions": [
                    "Add another word or two. Uncommon words are better."
                ]
            }
        }
    """

    data = flask.request.get_json(
        force=True,
    )
    dob = data['date_of_birth']

    # Check the password strength.
    strong, feedback = User.checkpwstrength(
        data['password'],
        data['username'],
        data['email'],
    )

    if not strong:
        return ({
            'status': 'failure',
            'username': data['username'],
            'message': 'Insufficiently secure password',
            'details': feedback,
        }, status.HTTP_400_BAD_REQUEST)


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


@app.route('/api/v<int:version>/auth/', methods=['POST'])
@app.route('/api/v<int:version>/login/', methods=['POST'])
def login(version):
    """Login.

    :query version: The version of the API currently in use.

    :<json string username: The login username.

    :<json string password: The user's password.

    :>json boolean success: ``True`` or ``False``.

    :>json string message: A message if success is ``False``.

    :>json string access_token: The access token for future requests.

    :statuscode 200: Success

    :statuscode 401: Invalid credentials.

    **Example request**:

    .. http:example:: curl

        POST /api/v0/login/ HTTP/1.0
        Accept: application/json
        Content-Type: application/json

        {
            "username": "user",
            "password": "pass"
        }

    **Example success**:

    Note that the access token is truncated here.

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        {
            "success": true,
            "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJ...8QWJFcYlI"
        }

    **Example failure**:

    .. sourcecode:: http

        HTTP/1.0 401 UNAUTHORIZED
        Content-Type: application/json

        {
            "success": false,
            "message": "Invalid credentials"
        }
    """
    data = request.get_json(force=True)

    username = data.get('username', None)
    password = data.get('password', None)

    if not (username and password):
        return (
            {
                'success': False,
                'message': 'Invalid request JSON',
            },
            status.HTTP_401_UNAUTHORIZED,
        )

    identity = jwt.authentication_callback(username, password)

    if identity:
        access_token = jwt.jwt_encode_callback(identity)
        return {
            'success': True,
            'access_token': access_token,
        }
    else:
        return (
            {
                'success': False,
                'message': 'Invalid credentials',
            },
            status.HTTP_401_UNAUTHORIZED,
        )
