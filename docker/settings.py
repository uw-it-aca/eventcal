# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from .base_settings import *
import os

INSTALLED_APPS += [
    'accountsynchr.apps.EventCalConfig',
]

LOGGING['formatters'] = {
    'std': {
        'format': '%(name)s %(levelname)-4s %(asctime)s %(message)s',
    },
}
LOGGING['handlers']['stdout']['formatter'] = 'std'
LOGGING['handlers']['stderr']['formatter'] = 'std'

DEBUG = False
if os.getenv('ENV') != 'localdev':
    CSV_FILE_PATH = '/csv'
    DEBUG = True

EMAIL_ADDRESS_DOMAIN = '@uw.edu'

RESTCLIENTS_DAO_CACHE_CLASS = None

LOGGING['formatters'] = {
    'std': {
        'format': '%(name)s %(levelname)-4s %(asctime)s %(message)s',
    },
}
LOGGING['handlers']['stdout']['formatter'] = 'std'
LOGGING['handlers']['stderr']['formatter'] = 'std'
