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

import flask_api
import flask_cors

app = flask_api.FlaskAPI(
    'hapcat',
)

flask_cors.CORS(
    app,
    expose_headers='Authorization'
)

import hapcat.apiserver
