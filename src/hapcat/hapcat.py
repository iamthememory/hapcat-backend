#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This module does stuff.
"""

from __future__ import absolute_import, print_function

import sys
import hapcat.apiserver


def main():
    """Start the Hapcat daemon.
    """

    print('Initializing Hapcat daemon...')

    hapcat.apiserver.daemon_listen()


if __name__ == '__main__':
    sys.exit(main())
