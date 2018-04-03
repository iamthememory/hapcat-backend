#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Hapcat configuration parser.
"""

from __future__ import absolute_import

from pkg_resources import resource_string

import configparser

def create_config(conffile):
    """Write the example configuration to the given file.
    """

    exconf = resource_string('hapcat', 'data/hapcatd-example.conf').decode()
    conffile.write(exconf)

def parse_config(conffile=None):
    """Load the configuration from the given file.
    """

    # Initialize our parser.
    config = configparser.ConfigParser(
        delimiters=('=',),
        comment_prefixes=('#',),
        inline_comment_prefixes=None,
        strict=True,
        interpolation=configparser.ExtendedInterpolation()
    )

    # Now, read our (minimal) default values.
    # These will be overwritten by the specified configuration.
    defaults = resource_string('hapcat', 'data/hapcatd-defaults.conf').decode()
    config.read_string(defaults, source='<hapcatd-defaults>')

    # Now, read our given configuration.

    if conffile:
        config.read_file(conffile)

    return config
