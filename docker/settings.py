from .base_settings import *
import os

ALLOWED_HOSTS = ['*']

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
            'callback': lambda record: record.levelno < logging.WARNING
        },
        'stderr_stream': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': lambda record: record.levelno > logging.ERROR
        }
    },
    'formatters': {
        'standard': {
            'format': '%(levelname)-4s %(asctime)s %(message)s [%(name)s]',
            'datefmt': '[%Y-%m-%d %H:%M:%S]',
        },
        'restclients_timing': {
            'format': '%(levelname)-4s restclients_timing %(module)s %(asctime)s %(message)s [%(name)s]',
            'datefmt': '[%Y-%m-%d %H:%M:%S]',
        },
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
        'eventcal.commands': {
            'handlers': ['stdout'],
            'level': 'INFO',
            'propagate': False,
        },
        '': {
            'handlers': ['stdout'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}

EVENTCAL_ADMIN_GROUP = os.getenv('ADMIN_GROUP')
#CSV_FILE_PATH = '/data/eventcal/csv'

if os.getenv('ENV', 'localdev') == 'prod':
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
else:
    EMAIL_BACKEND = 'saferecipient.EmailBackend'
    SAFE_EMAIL_RECIPIENT = os.getenv('SAFE_EMAIL_RECIPIENT')
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = 587
EMAIL_TIMEOUT = 15
EMAIL_ADDRESS_DOMAIN = '@uw.edu'
EMAIL_SENDER = os.getenv('EMAIL_SENDER', 'uweventcalweb@uw.edu')
EMAIL_SSL_CERTFILE = os.getenv('CERT_PATH', '')
EMAIL_SSL_KEYFILE = os.getenv('KEY_PATH', '')
PURGE_EMAIL_MESSAGE = 'Greetings!\n\nYou are receiving this message because you have an editor account in Trumba (campus event calendars) that has been inactive for over a year. Upon the recommendation of the vendor, we will regularly close unused editor accounts.\n\nYour account is scheduled to be deleted on Aug 2, 2020. If you wish to remain an editor, simply log into http://trumba.uw.edu/ with your UW NetID before then. Otherwise no action is needed.\n\nContact us at help@uw.edu if you have any questions.\n\nBest,\nThe UW campus event calendars team\n'
PURGE_EMAIL_SUBJECT = 'Your Trumba Account Will Be Closed'
