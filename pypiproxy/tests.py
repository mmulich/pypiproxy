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

    def setUp(self):
        # Intercept all httplib2 requests
        httplib2_intercept.install()
        import httplib2
        # Fix for httplib2 >= 0.7
        httplib2_SCHEME_TO_CONNECTION = httplib2.SCHEME_TO_CONNECTION.copy()
        httplib2.SCHEME_TO_CONNECTION = {
            'http': httplib2.HTTPConnectionWithTimeout,
            'https': httplib2.HTTPSConnectionWithTimeout
            }
        # Cleanup the interception
        self.addCleanup(httplib2_intercept.uninstall)
        self.addCleanup(setattr, httplib2, 'SCHEME_TO_CONNECTION',
                        httplib2_SCHEME_TO_CONNECTION)

    def add_intercept(self, host='pypi.python.org', port=80, app=None):
        """Intercept requests that match the given host and port."""
        if app is None:
            app = testing.fake_app
        wsgi_intercept.add_wsgi_intercept(host, port, app)
        self.addCleanup(wsgi_intercept.remove_wsgi_intercept, host, port)

    def test_for_wsgi_response(self):
        pass

    def test_proxies(self):
        self.add_intercept()
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
        def four0four_app(environ, start_response):
            start_response('404 Not Found',
                           [('Content-type', 'text/plain')])
            return ["Dude, where's my car?"]
        app = testing.empty_wrapper(four0four_app)
        self.add_intercept(app=app)
        # Create the request
        environ = {'PATH_INFO': '/simple/sake/',
                   'wsgi.url_scheme': 'http',
                   }
        request = Request(environ)

        from pypiproxy.main import PyPIProxy
        app = PyPIProxy()
        response = app.respond(request)
        self.assertEqual(response.status, '404 Not Found')
        self.assertTrue(response.body.find('car') >= 0)

    def test_proxies_302(self):
        pass


class CachedTestCase(unittest.TestCase):
    """Test for caching Packages but not the index itself."""
