#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""Setup and/or install Hapcat Backend.
"""

# Author: Alex Corkwell, with (labeled) portions from the tox
#         documentation.

# Trying to build a Windows installer on non-Windows systems fails,
# since distutils tries to use the mbcs codec, which isn't a real codec,
# but just an alias for the current codec on a Windows system.
# If the codec doesn't exist, register ascii in its place.
# From <http://code.activestate.com/lists/python-list/616822/>.

import codecs
try:
    codecs.lookup('mbcs')
except LookupError:
    ascii = codecs.lookup('ascii')
    # This lambda returns ascii if name is 'mbcs', else None.
    # It keeps the evaluated value of ascii by passing it as a default.
    func = lambda name, enc=ascii: {True: enc}.get(name == 'mbcs')
    codecs.register(func)

# Trying to build a 64-bit Windows installer on non-Windows systems
# fails, because the MSVC version defaults to 6 if it can't find the
# Visual Studio version that Python was built with (because it's not on
# Windows).
# The 64-bit installer executable only exists for MSVC 9.0 and later.
# Every Python version from 2.6.0 on has had at least MSVC 9.0.
# So, it is reasonably safe to redefine the version if it's the default
# of 6.
# This should only fail for odd custom builds, and Python versions
# before 2.6, which we don't support anyway.
# Note that, for various reasons, this returns a float (if it's not 6).
# This is not a typo.

import distutils.msvccompiler
if distutils.msvccompiler.get_build_version() == 6:
    distutils.msvccompiler.get_build_version = lambda: 9.0

import io
from os.path import dirname, join
from setuptools import setup, find_packages

# The following is an example from the tox documentation on running
# tox from ``setup.py test``.
# <https://testrun.org/tox/latest/example/basic.html>
from setuptools.command.test import test as TestCommand
import sys


class Tox(TestCommand):

    user_options = [('tox-args=', 'a', 'Arguments to pass to tox')]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # Import here, because the eggs aren't loaded by setuptools
        # before this point if the user doesn't have tox installed.
        import tox
        import shlex
        args = self.tox_args
        if args:
            args = shlex.split(self.tox_args)
        errno = tox.cmdline(args=args)
        sys.exit(errno)

authors = ', '.join([
    'Alex Corkwell <i.am.the.memory@gmail.com>',
    'Christopher Herzog <cherzog@kent.edu>',
    'Justin Boey <jrboey98@gmail.com>',
    'Kyle Raney <kraney@kent.edu>',
])

# Build the long description from the README and CHANGELOG.
# Make sure we build the path relative to this file, in case we're run
# from outside the directory.
# We use io.open so we can portably (Python 2/3) read the files as
# utf-8.

# Get the README.
readmefile = io.open(join(dirname(__name__), 'README.rst'), encoding='utf8')
readme = readmefile.read()
readmefile.close()

# Get the CHANGELOG.
changefile = io.open(join(dirname(__name__), 'CHANGELOG.rst'), encoding='utf8')
changes = changefile.read()
changefile.close()

# Build the description.
long_desc = '%s\n\n%s' % (readme, changes)

setup(
    name='hapcat',
    version='0.0.1',
    description='The backend code for the Hapcat Project',
    long_description=long_desc,
    author=authors,
    author_email=authors,
    url='https://github.com/iamthememory/hapcat',
    package_dir={'hapcat': 'src/hapcat'},
    packages=['hapcat'],
    py_modules=[],
    package_data={'hapcat': ['data/*']},
    tests_require=[
        'tox',
        'httpstatus35;python_version<"3.5"',
        'enum34;python_version<"3.4"',
    ],
    install_requires=[
        'httpstatus35;python_version<"3.5"',
        'enum34;python_version<"3.4"',
    ],
    cmdclass={
        'test': Tox,
    },
    entry_points={
        'console_scripts': [
            ]
        }
)
