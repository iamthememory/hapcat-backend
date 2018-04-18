#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Hapcat API server module.
"""

from __future__ import absolute_import

from pkg_resources import resource_string

import hapcat

from hapcat import app
from flask import json
import flask

from flask.ext.api.decorators import set_renderers
from flask.ext.api.renderers import JSONRenderer, HTMLRenderer

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

def daemon_listen(config, engine, sessionfact):
    """Listen and handle API requests.
    """

    app.run(
        host=config.get('apiserver', 'address'),
        port=config.getint('apiserver', 'port'),
    )

