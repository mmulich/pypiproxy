# -*- coding: utf-8 -*-
import os
import httplib2
from webob import Request, Response


class PyPIProxy(object):
    """Main WSGI proxy application"""

    def __init__(self, host='pypi.python.org', scheme='http', port=80,
                 **local_config):
        self.host = host
        self.scheme = scheme
        self.port = isinstance(port, str) and int(port) or port

    def __call__(self, environ, start_response):
        """Simplify the WSGI stuff here."""
        request = Request(environ)
        response = self.respond(request)
        return response(environ, start_response)

    def respond(self, request):
        address_parts = dict(scheme=self.scheme,
                             host=self.host,
                             port=self.port,
                             path=request.path,
                             )
        address = "{scheme}://{host}:{port!s}{path}".format(**address_parts)

        h = httplib2.Http()  ##'.cache') TODO Find a good location for cached data.
        # TODO Use HTTP cache-control headers.

        # Request the information from our proxy
        resp, content = h.request(address)
        response = Response()
        response.headerlist = resp.items()
        response.body = content
        return response
