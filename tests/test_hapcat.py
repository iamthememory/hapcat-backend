#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test the hapcat.hapcat module.

This module may be run in several ways.

The preferred method is to use tox in the root directory of the source
tree.
tox can take care of all the details easily.

Alternatively, this module can be run directly, which may be more
prone to issues, and doesn't nice and pretty output.

See README.rst for details.
"""

import unittest

# If this file is run directly by a user we need to shove the path of the src
# directory onto Python's path.
# Try to import the module first, though.
try:
    import hapcat.hapcat
except ImportError:
    # Put the src directory into the path and try to import again.
    import path_hack
    path_hack.put_src_on_path()
    import hapcat.hapcat


class TestThing(unittest.TestCase):
    """Test something.
    """

    def setUp(self):
        """Set up the data for the tests.
        """

        pass

    def test_thing_about_thing(self):
        """Test something about the thing we're testing.
        """

        pass


if __name__ == '__main__':
    unittest.main()
