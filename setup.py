# -*- coding: utf-8 -*-
"""\
A Proxy / Caching application for Python Package Indexes.
"""
import os
import sys
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

name = 'pypiproxy'
version = '1.0a1'

install_requires = [
    'setuptools',
    'WebOb',
    'httplib2',
    ]
test_requires = [
    'wsgi_intercept',
    ]
if sys.version_info < (2, 7,):
    test_requires.append('unittest2')
extras_require = {'test': test_requires}

description = __doc__
long_description = '\n\n'.join([
        read('README.rst'),
        read('docs', 'changes.rst'),
])
url = ''

entry_points = """\
"""

DEV_STATES = [
    "Development Status :: 3 - Alpha",
    "Development Status :: 4 - Beta",
    "Development Status :: 5 - Production/Stable",
]
if version.find('a') >= 0:
    state = 0
elif version.find('b') >= 0:
    state = 1
else:
    state = 2
development_status = DEV_STATES[state]

setup(
    name=name,
    version=version,
    author="Michael Mulich",
    author_email="michael.mulich@gmail.com",
    description=description,
    long_description=long_description,
    url=url,
    classifiers=["Framework :: Plone",
                 "Programming Language :: Python",
                 "Intended Audience :: Developers",
                 development_status,
                 ],
    keywords='plone buildout',
    license='GPL',
    packages=find_packages(),
    install_requires=install_requires,
    extras_require=extras_require,
    include_package_data=True,
    zip_safe=False,
    entry_points=entry_points,
    )
