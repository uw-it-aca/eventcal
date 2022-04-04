# Copyright 2022 UW-IT, University of Washington
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

if os.getenv('ENV') != 'localdev':
    CSV_FILE_PATH = '/csv'

if os.getenv('ENV', 'localdev') == 'prod':
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
else:
    EMAIL_BACKEND = 'saferecipient.EmailBackend'
    SAFE_EMAIL_RECIPIENT = os.getenv('SAFE_EMAIL_RECIPIENT')
EMAIL_ADDRESS_DOMAIN = '@uw.edu'
EMAIL_USE_TLS=True
EMAIL_SSL_CERTFILE = os.getenv('CERT_PATH', '')
EMAIL_SSL_KEYFILE = os.getenv('KEY_PATH', '')
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = 587
EMAIL_TIMEOUT = 60

RESTCLIENTS_DAO_CACHE_CLASS = None
