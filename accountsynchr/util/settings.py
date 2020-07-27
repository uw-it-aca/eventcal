import os
from django.conf import settings


def get_csv_file_path():
    return getattr(settings, 'CSV_FILE_PATH', None)


def get_email_address_domain():
    return getattr(settings, 'EMAIL_ADDRESS_DOMAIN', None)


def get_email_sender():
    return getattr(settings, 'EMAIL_SENDER', None)


def get_email_message():
    return getattr(settings, 'PURGE_EMAIL_MESSAGE', None)


def get_email_subject():
    return getattr(settings, 'PURGE_EMAIL_SUBJECT', None)


def get_cronjob_sender():
    return getattr(settings, 'CRONJOB_SENDER', 'trumba_cron')
