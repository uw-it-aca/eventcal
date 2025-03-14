# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


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


def get_cronjob_sender():
    return "{}{}".format(
        getattr(settings, 'CRONJOB_SENDER', 'trumba-cron'),
        get_email_address_domain())


def get_recent_editor_duration():
    return getattr(settings, 'RECENT_EDITOR_DURATION', 30)


def get_account_inactive_duration():
    return getattr(settings, 'ACCOUNT_INACTIVE_DURATION', 365)
