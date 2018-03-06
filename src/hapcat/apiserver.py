#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Hapcat API server module.
"""

from __future__ import absolute_import

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
        self.end_headers()
        self.wfile.write(data)

    @staticmethod
    def sanitize_url(path):
        """Sanitize a URL to turn it into the canonical URL.
        """

        return path

    def suggestions(self):
        """Retrieve suggestions.
        """

        data = 'Suggestions here'.encode()
        code = HTTPStatus.OK

        return code, data

    handlers = {
        '/suggestions': suggestions,
    }


if __name__ == '__main__':
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, APIRequestHandler)
    httpd.serve_forever()
