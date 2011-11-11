# -*- coding: utf-8 -*-

_app_was_hit = False

def has_been_hit():
    return _app_was_hit

def simple_app(environ, start_response):
    """Simplest possible application object"""
    status = '200 OK'
    response_headers = [('Content-type','text/plain')]
    start_response(status, response_headers)

    global _app_was_hit
    _app_was_hit = True

    body = """\
WSGI intercept successful!
HTTP_HOST: %s
PATH_INFO: %s
""" % (environ['HTTP_HOST'], environ['PATH_INFO'])
    return [body]

def fake_app():
    global _app_was_hit
    _app_was_hit = False
    return simple_app
