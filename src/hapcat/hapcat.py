#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This module does stuff.
"""

from __future__ import absolute_import, print_function

import argparse
import sys

import hapcat
import hapcat.db
import hapcat.apiserver
import hapcat.config


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

    # Parse our arguments.
    args = make_argparser().parse_args()

    if args.genconfig:
        hapcat.config.create_config(args.genconfig)
        return

    # Parse/generate our configuration.
    config = hapcat.config.parse_config(args.config)

    del args

    print('Initializing database...')

    engine, sessionfact = hapcat.db.initdb(config.get('database', 'dburl'))

    print('Initializing Hapcat daemon...')

    hapcat.apiserver.daemon_listen(config, engine, sessionfact)


if __name__ == '__main__':
    sys.exit(main())
