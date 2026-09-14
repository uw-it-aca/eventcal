# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import os
from setuptools import setup

README = """
See the README on `GitHub
<https://github.com/uw-it-aca/eventcal>`_.
"""

version_path = 'accountsynchr/VERSION'
VERSION = open(os.path.join(os.path.dirname(__file__), version_path)).read()
VERSION = VERSION.replace("\n", "")

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='EventCal',
    version=VERSION,
    packages=['accountsynchr'],
    author="UWIT Student & Educational Technology Services",
    author_email="aca-it@uw.edu",
    include_package_data=True,
    install_requires=[
        'django~=5.2',
        'uw-memcached-clients~=1.1',
        'uw-restclients-core~=1.4',
        'uw-restclients-gws~=2.3',
        'uw-restclients-space~=1.2',
        'uw-restclients-trumba~=1.4',
        'django-safe-emailbackend~=1.2',
        'lxml>=6,<7',
        'psycopg[c]',
    ],
    license='Apache License, Version 2.0',
    description=('App synchronizes UW calendar groups and Trumba permissions'),
    long_description=README,
    url="https://github.com/uw-it-aca/eventcal",
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
