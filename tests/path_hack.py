# -*- coding: utf-8 -*-

# Author: Alex Corkwell

"""Put the src directory into Python's module lookup path.

This module inserts the src directory, which contains the modules and
packages, into Python's path.
It is intended for when Python cannot find the modules to be tested,
normally because the user is running tests in an odd manner.

Example:
    To use, first try to import a module, such as ``mod_a``.
    If that fails, import this module, run the following and try to
    import again. ::

        try:
            import mod_a
        except ImportError:
            import path_hack
            path_hack.put_src_on_path()
            import mod_a

    If this fails, the module does not exist, or the user is doing
    something wrong.
"""

import os.path
import sys


def put_src_on_path():
    """Put the src directory into the path.

    When called, this attempts to put the absolute path of the ``src``
    directory into Python's path.
    Assuming that this function is defined in ``$D/tests/path_hack.py``,
    this will be the absolute path of ``$D/src``.
    This directory is inserted at the beginning of the path, which
    will override system modules and packages with the same names as
    those in ``src``.

    If ``src`` does not exist, having it in the path does not appear to
    cause any apparent issues, although this has not been thoroughly
    verified.

    This function will not insert the ``src`` directory into the path
    again if its absolute path is already there.
    This makes it safe to call this function multiple times,
    possibly from different modules.
    It does not, however, detect duplicates by links or relative paths,
    so it does not protect from duplicates if code modifies ``sys.path``
    in multiple places, although these duplicates should have little
    real effect on execution.

    Currently, this function uses its module's filename to find the
    ``src`` directory.
    This is not necessarily robust, and so it is preferred that the test
    suite be run from some test runner, rather than the tests being
    run directly.
    """

    # Get the absolute path of this file.
    # This removes any potential issues with odd setups and relative
    # paths later.
    test_path = os.path.abspath(__file__)

    # The root of the source tree is up two directories.
    src_root = os.path.dirname(os.path.dirname(test_path))

    # Put the src directory into the front of Python's module lookup
    # path.
    # We could put it at the end, but 'stats' seems like a common name
    # which could be easily blocked by a module elsewhere on the system.
    src_path = os.path.join(src_root, 'src')

    # Don't add the directory if it's already there.
    if src_path not in sys.path:
        sys.path.insert(0, src_path)
