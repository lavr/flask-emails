#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import os
import re
import sys
import ast

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

settings = dict()

# Publish Helper.
if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

from setuptools import Command, setup


def find_version(path):
    _version_re = re.compile(r'__version__\s+=\s+(.*)')
    with open(path, 'rb') as f:
        return str(ast.literal_eval(_version_re.search(
            f.read().decode('utf-8')).group(1)))


settings.update(
    name='flask-emails',
    version=find_version('flask_emails/__init__.py'),
    description='Elegant and simple email library for Flask.',
    long_description=open('README.rst').read(),
    author='Sergey Lavrinenko',
    author_email='s@lavr.me',
    url='https://github.com/lavr/flask-emails',
    packages=['flask_emails', ],
    install_requires=['emails', ],
    license=open('LICENSE').read(),
    zip_safe=False,
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Communications",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Other/Nonlisted Topic",
        "Topic :: Software Development :: Libraries :: Python Modules",
    )
)


setup(**settings)
