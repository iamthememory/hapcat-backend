# -*- coding: utf-8 -*-

# Author: Alex Corkwell

"""Put the source directory into Python's module lookup path.

This module inserts the source directory, which contains the modules and
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
    """Put the source directory into the path.
    """

    test_path = os.path.abspath(__file__)

    src_root = os.path.dirname(os.path.dirname(test_path))

    if src_root not in sys.path:
        sys.path.insert(0, src_root)
