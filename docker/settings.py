from .base_settings import *
import os

INSTALLED_APPS += [
    'accountsynchr.apps.EventCalConfig',
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'stdout_stream': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': lambda record: record.levelno <= logging.WARNING
        },
        'stderr_stream': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': lambda record: record.levelno >= logging.ERROR
        }
    },
    'formatters': {
        'standard': {
            'format': '%(name)s %(levelname)-4s %(asctime)s %(message)s',
        }
    },
    'handlers': {
        'stdout': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'filters': ['stdout_stream'],
            'formatter': 'standard',
        },
        'stderr': {
            'class': 'logging.StreamHandler',
            'stream': sys.stderr,
            'filters': ['stderr_stream'],
            'formatter': 'standard',
        },
    },
    'loggers': {
        '': {
            'handlers': ['stdout', 'stderr'],
            'level': 'INFO',
        },
    }
}

if os.getenv('ENV') != 'localdev':
    CSV_FILE_PATH = '/app/csv'

if os.getenv('ENV', 'localdev') == 'prod':
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
else:
    EMAIL_BACKEND = 'saferecipient.EmailBackend'
    SAFE_EMAIL_RECIPIENT = os.getenv('SAFE_EMAIL_RECIPIENT')
EMAIL_ADDRESS_DOMAIN = '@uw.edu'
EMAIL_SSL_CERTFILE = os.getenv('CERT_PATH', '')
EMAIL_SSL_KEYFILE = os.getenv('KEY_PATH', '')
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = 587
EMAIL_TIMEOUT = 60
