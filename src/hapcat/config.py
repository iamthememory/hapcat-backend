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
