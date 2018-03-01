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

dummy = '<html><head><title>Success!</title></head><body>Success!</body></html>'


class APIRequestHandler(BaseHTTPRequestHandler):
    """Handle API server requests.
    """

    server_version = 'Hapcat/' + hapcat.__version__

    def do_GET(self):
        """Handle a GET request.
        """

        data = dummy.encode()

        self.send_response(HTTPStatus.OK)
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)


if __name__ == '__main__':
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, APIRequestHandler)
    httpd.serve_forever()
