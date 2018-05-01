Changelog
=========

Version 0.0.3
-------------

Fixes:

- Change ``location`` and ``event`` in ``order`` to their proper plurals

Version 0.0.2
-------------

Features:

- Use globally unique IDs
- Document the HTTP API in Sphinx
- Add events
- Add URLs to query a tag, event, or location
- Generate suggestions from the database
- Add a ``/debug/dropalldata/`` URL to drop data in debugging
- Add photos for locations and events

API Changes:

- Move ``/reloadtestdata/`` to ``/debug/reloadtestdata/``

Version 0.0.2.dev10
-------------------

Fixes:

- Only attempt to load configuration from the command line if given
- Correct the ``__future__`` module typo.

Features:

- Add uWSGI configuration to the hapcat configuration

Version 0.0.2.dev9
------------------

Fixes:

- Fix absolute imports on Python 2.7
- Fix the database URI not being loaded when run as ``hapcat -c <config>``

Version 0.0.2.dev8
------------------

Fixes:

- Fix the dbutil import in hapcat.py after the module rename

Version 0.0.2.dev7
------------------

Fixes:

- Fix a syntax error in setup.py

Version 0.0.2.dev6
------------------

Features:

- Move to Flask-API
- Add a user table
- Add a user registration URL
- Add a URL to reload test data

Version 0.0.2.dev5
------------------

Fixes:

- Adjust package_data so wheel creation works

Version 0.0.2.dev4
------------------

Features:

- Add basic database support
- Add database migration support
- Load initial test data for implemented models
- Add tags table
- Add locations table

Fixes:

- Adjust package_dir so develop mode actually works properly

New dependencies:

- Alembic
- SQLAlchemy

Version 0.0.2.dev3
------------------

Features:

- Add CORS header to allow browsers to load data

Version 0.0.2.dev2
------------------

Features:

- Add config file support
- Add argument parsing

API changes:

- Change type to section in JSON

Version 0.0.2.dev1
------------------

Features:

- Add server info
- Add debugging URLS

Version 0.0.2.dev0
------------------

- Beginning of new versioning system

Version 0.0.1 (Unreleased)
--------------------------

- Testing only
