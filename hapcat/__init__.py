# -*- coding: utf-8 -*-

"""The Hapcat Backend package.
"""

from __future__ import (
    absolute_import,
    division,
)

__version__ = '0.0.4.dev0'

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
import flask_migrate
import flask_sqlalchemy
import os
import os.path
import pkg_resources
import sys

try:
    import secrets
except ImportError:
    # Import the small module hackily copied from the Python 3.6 library, since
    # no one seems to have backported it on PyPI yet.
    import hapcat.compat.secrets as secrets


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

app.config['SQLALCHEMY_DATABASE_URI'] = app.iniconfig.get('database', 'dburl')

db = flask_sqlalchemy.SQLAlchemy(app)

migrate = flask_migrate.Migrate(
    app,
    db,
    directory=pkg_resources.resource_filename('hapcat', 'migrations'),
)


flask_cors.CORS(
    app,
    expose_headers='Authorization'
)

import hapcat.apiserver
import hapcat.models

if os.path.basename(sys.argv[0]) not in ['sphinx-build', 'sphinx-build.exe']:
    with app.app_context():
        flask_migrate.upgrade()

def makejwtsecret(bits=512):
    """Read or generate the JWT secret.
    """

    key = u'jwtsecret'

    from hapcat.models import Secret

    # First try to get the secret.
    secret = db.session.query(Secret).filter(Secret.id == key).first()

    if secret:
        return secret.payload

    payload = secrets.token_bytes(bits // 8)

    secret = Secret(id=key, payload=payload)

    db.session.add(secret)
    db.session.commit()

    return secret.payload

jwtsecret = makejwtsecret()
