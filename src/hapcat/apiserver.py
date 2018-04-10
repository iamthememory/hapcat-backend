#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Hapcat API server module.
"""

from __future__ import absolute_import

import json
from pkg_resources import resource_string

try:
    from http import HTTPStatus
except ImportError:
    from httpstatus import HTTPStatus

try:
    from http.server import BaseHTTPRequestHandler, HTTPServer
except ImportError:
    from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

import hapcat


class APIRequestHandler(BaseHTTPRequestHandler):
    """Handle API server requests.
    """

    server_version = 'Hapcat/' + hapcat.__version__

    def do_GET(self):
        """Handle a GET request.
        """

        url = self.sanitize_url(self.path)

        # Get the handler.
        try:
            handler = self.handlers[url]
            code, data = handler(self)

        except KeyError:
            code = HTTPStatus.NOT_FOUND
            data = 'Unknown API URL'.encode()

        self.send_response(code)
        self.send_header('Content-Length', str(len(data)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(data)

    @staticmethod
    def sanitize_url(path):
        """Sanitize a URL to turn it into the canonical URL.
        """

        return path

    def suggestions(self):
        """Retrieve suggestions.

        FIXME: Don't use test data.
        """

        # Simulate creating and encoding JSON, instead of just sending the file
        # as-is.
        sugs = resource_string('hapcat', 'data/test-suggestions.json')
        sugs = json.loads(sugs.decode())

        data = json.dumps(sugs).encode()
        code = HTTPStatus.OK

        return code, data

    def serverinfo(self):
        """Send server info.
        """

        info = {
            'server_version': hapcat.__version__,
            'api_versions': [0],
        }

        data = json.dumps(info).encode()
        code = HTTPStatus.OK

        return code, data

    def send_error(self, *args, **kwargs):
        """Send and log an error reply.

        Arguments are

        * code:    an HTTP error code
                   3 digits
        * message: a simple optional 1 line reason phrase.
                   \*( HTAB / SP / VCHAR / %x80-FF )
                   defaults to short entry matching the response code
        * explain: a detailed message defaults to the long entry
                   matching the response code.

        This sends an error response (so it must be called before any
        output has been generated), logs the error, and finally sends
        a piece of HTML explaining the error to the user.

        This is a copy of the upstream with fixed formatting to prevent
        Sphinx from choking up.
        """

        BaseHTTPRequestHandler.send_error(self, *args, **kwargs)

    def debug_urls(self):
        """Send a list of URLs for debugging.
        """

        basetemp = """\
<html>
    <head>
        <title>
            URLs list (debugging)
        </title>
    </head>
    <body>
        <ul>
%s
        </ul>
    </body>
</html>\
"""

        itemplate = """\
            <li>
                <a href="%(url)s">%(urltext)s</a>
            </li>\
"""

        urllist = []

        for handler in sorted(self.handlers.keys()):
            d = {
                'url': handler,
                'urltext': handler + ': ' + self.handlers[handler].__name__,
            }
            urllist.append(itemplate % d)

        text = (basetemp % '\n'.join(urllist)).encode()

        return HTTPStatus.OK, text

    handlers = {
        '/': debug_urls,
        '/api/serverinfo': serverinfo,
        '/api/v0/serverinfo': serverinfo,
        '/api/v0/suggestions': suggestions,
    }


def daemon_listen(config):
    """Listen and handle API requests.
    """

    httpd = HTTPServer(
        (
            config.get('apiserver', 'address'),
            config.getint('apiserver', 'port')
        ),
        APIRequestHandler
    )
    httpd.serve_forever()
