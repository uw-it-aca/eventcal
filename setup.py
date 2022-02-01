# Copyright 2022 UW-IT, University of Washington
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
    author="UW-IT AXDD",
    author_email="aca-it@uw.edu",
    include_package_data=True,
    install_requires=[
        'Django~=2.2.24',
        'lxml==4.6.5',
        'uw-memcached-clients~=1.0.10',
        'UW-RestClients-Core~=1.3.8',
        'UW-RestClients-GWS~=2.3.4',
        'UW-RestClients-Trumba~=1.3.7',
        'Django-Safe-EmailBackend~=1.2',
        ],
    license='Apache License, Version 2.0',
    description=('App synchronizes uw calendar groups and Trumba permissions'),
    long_description=README,
    url="https://github.com/uw-it-aca/eventcal",
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
    ],
)
