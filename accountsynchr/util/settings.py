import os
from django.conf import settings


def get_csv_file_path():
    return getattr(settings, 'CSV_FILE_PATH', None)


def get_email_address_domain():
    return getattr(settings, 'EMAIL_ADDRESS_DOMAIN', None)


def get_user_email_sender():
    return "{}{}".format(
        getattr(settings, 'EMAIL_SENDER', 'uweventcalweb'),
        get_email_address_domain())


def get_next_purge_date():
    return getattr(settings, 'PURGE_DATE', None)


def get_cronjob_sender():
    return "{}{}".format(
        getattr(settings, 'CRONJOB_SENDER', 'trumba_cron'),
        get_email_address_domain())
