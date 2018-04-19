#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The main hapcat entrypoints.
"""

from __future__ import absolute_import, print_function

import argparse
import os
import sys

import hapcat
import hapcat.apiserver
import hapcat.config
import hapcat.dbutil


def make_argparser():
    """Return an ArgumentParser for hapcatd.
    """

    parser = argparse.ArgumentParser(
        description=hapcat.__description__,
        add_help=True
    )

    # Version.
    parser.add_argument(
        '-V',
        '--version',
        action='version',
        version='%(prog)s {version}'.format(version=hapcat.__version__)
    )

    confgroup = parser.add_mutually_exclusive_group()

    confgroup.add_argument(
        '-c',
        '--config',
        type=argparse.FileType('r'),
        help='the configuration file to use'
    )

    confgroup.add_argument(
        '-g',
        '--genconfig',
        type=argparse.FileType('w'),
        help='generate a default configuration file'
    )

    return parser

def main():
    """Start the Hapcat daemon.
    """

    from hapcat import app

    # Parse our arguments.
    args = make_argparser().parse_args()

    if args.genconfig:
        hapcat.config.create_config(args.genconfig)
        return

    # Load our non-environment configuration.

    with app.app_context():
        app.iniconfig.readfp(args.config)

    del args

    app.run(
        host=app.iniconfig.get('apiserver', 'address'),
        port=app.iniconfig.getint('apiserver', 'port'),
    )


if __name__ == '__main__':
    sys.exit(main())
