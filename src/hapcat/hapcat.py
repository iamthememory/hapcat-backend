#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This module does stuff.
"""

from __future__ import absolute_import, print_function

import argparse
import sys

import hapcat
import hapcat.apiserver


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

    return parser

def main():
    """Start the Hapcat daemon.
    """

    # Parse our arguments.
    args = make_argparser().parse_args()

    print('Initializing Hapcat daemon...')

    hapcat.apiserver.daemon_listen()


if __name__ == '__main__':
    sys.exit(main())
