import os
from setuptools import setup

README = """
See the README on `GitHub
<https://github.com/uw-it-aca/eventcal>`_.
"""

# The VERSION file is created by travis-ci, based on the tag name
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
        'Django>=2.0.13,<2.1',
        'UW-RestClients-Core>1.2,<2.0',
        'UW-RestClients-GWS>=2.2.1,<3.0',
        'UW-RestClients-Trumba>=1.3.1,<2.0',
        'pyopenssl'
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
