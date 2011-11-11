# -*- coding: utf-8 -*-
import sys
try:
    import unittest2 as unittest
except ImportError:
    if sys.version_info <= (2, 6):
        raise RuntimeError("These tests require unittest2")
    else:
        # Python 2.7 unittest == unittest2
        import unittest
from wsgiref.util import setup_testing_defaults
from webob import Request
import wsgi_intercept
from wsgi_intercept import httplib2_intercept
from pypiproxy import testing

class ProxyTestCase(unittest.TestCase):
    """Test the application proxies requests."""

    def test_for_wsgi_response(self):
        pass

    def test_proxies(self):
        # Intercept requests to the default index.
        httplib2_intercept.install()
        import httplib2
        httplib2.SCHEME_TO_CONNECTION = {
            'http': httplib2.HTTPConnectionWithTimeout,
            'https': httplib2.HTTPSConnectionWithTimeout
            }
        wsgi_intercept.add_wsgi_intercept('pypi.python.org', 80,
                                          testing.fake_app)

        # Create the request
        environ = {'PATH_INFO': '/simple/sake/',
                   'wsgi.url_scheme': 'http',
                   }
        request = Request(environ)

        from pypiproxy.main import PyPIProxy
        app = PyPIProxy()
        response = app.respond(request)
        self.assertTrue(response.body.find('intercept') >= 0)
        self.assertTrue(testing.has_been_hit())

    def test_proxies_404(self):
        pass


class CachedTestCase(unittest.TestCase):
    """Test for caching Packages but not the index itself."""
