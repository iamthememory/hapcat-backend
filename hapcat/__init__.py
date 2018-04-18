# -*- coding: utf-8 -*-

"""The Hapcat Backend package.
"""

__version__ = '0.0.2.dev5'

__description__ = """\
The backend daemon for the hapcat project.
"""

__api_versions__ = [
    0,
]

import configparser
import flask_api
import flask_cors
import flask_ini
import os
import pkg_resources

app = flask_api.FlaskAPI(
    'hapcat',
)

with app.app_context():
    app.iniconfig = flask_ini.FlaskIni(
        delimiters=('=',),
        comment_prefixes=('#',),
        inline_comment_prefixes=None,
        strict=True,
        interpolation=configparser.ExtendedInterpolation()
    )

    app.iniconfig.read(
        pkg_resources.resource_filename('hapcat', 'data/hapcatd-defaults.conf')
    )

    envconf = os.environ.get('HAPCAT_FLASK_CONFIG', None)

    if envconf:
        app.iniconfig.read(envconf)


flask_cors.CORS(
    app,
    expose_headers='Authorization'
)

import hapcat.apiserver
