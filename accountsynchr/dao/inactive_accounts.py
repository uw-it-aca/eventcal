# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


import logging
import csv
import os
import re
from dateutil.parser import parse
from datetime import datetime, timedelta
from django.utils import timezone
from accountsynchr.util.settings import (
    get_csv_file_path, get_email_address_domain,
    get_recent_editor_duration, get_account_inactive_duration)
from accountsynchr.models import UserAccount
from accountsynchr.models.user import EditorCreation
from accountsynchr.dao.notifier import send_acc_removal_email

logger = logging.getLogger(__name__)


def get_file_path(filename='accounts.csv'):
    file_path = get_csv_file_path()
    if file_path is None:
        file_path = os.path.join(os.path.dirname(__file__), '..', 'data')
    return os.path.join(file_path, filename)


def get_accounts_to_purge(editor_group_members,
                          notify_inactive_users=False):
    """
    Identifies user accounts to be purged based on inactivity.
    Email users to be purged in the next run.
    returns: 1. a list of UserAccounts of the users to be purged
             2. a set of uwnetids of the users to be purged
    """
    recent_editor_cutoff = timezone.now() - timedelta(
        days=get_recent_editor_duration())
    recently_added_editors = EditorCreation.get_editors(recent_editor_cutoff)

    notify_cutoff = datetime.now() - timedelta(
        days=get_account_inactive_duration())
    purge_cutoff = notify_cutoff - timedelta(days=90)

    total_notified_users = 0
    total_notify_err = 0

    email_address_domain = get_email_address_domain()
    path = get_file_path()

    user_records = []  # store in a list
    user_set = set()  # store in a set

    with open(path, 'r', encoding='utf8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header row
        for line in reader:
            try:
                if line[2].endswith(email_address_domain):
                    last_visit = str_to_datetime(line[4])
                    uwnetid = re.sub(
                        email_address_domain, "", line[2], flags=re.I).lower()
                    acc = UserAccount(uwnetid=uwnetid, last_visit=last_visit)

                    if last_visit is not None:
                        if (last_visit < purge_cutoff and
                                uwnetid not in recently_added_editors):
                            # Will be purged in this run
                            user_records.append(acc)
                            user_set.add(acc.uwnetid)

                        elif (last_visit < notify_cutoff and
                                notify_inactive_users):
                            if send_acc_removal_email(acc.uwnetid):
                                total_notified_users += 1
                            else:
                                total_notify_err += 1
                    else:
                        # Has not accessed Trumba
                        if (uwnetid not in recently_added_editors and
                                uwnetid not in editor_group_members):
                            # Not purge those recently added to an editor group
                            # or still is a member in an editor group
                            user_records.append(acc)
                            user_set.add(acc.uwnetid)

            except Exception as ex:
                logger.error(f"{ex} in line: {line}")

    if notify_inactive_users:
        logger.info(f"Notified {total_notified_users} users")
        logger.info(
            f"{total_notify_err} errors occurred while sending " +
            "notification emails")

    return user_records, user_set


def str_to_datetime(s):
    return parse(s) if (s is not None and len(s)) else None


def get_accounts_to_purge1(editor_group_members,
                           notify_inactive_users=False):
    """
    Use Steve exported account file.
    Also email users to be purged in the next month.
    returns: 1. a list of UserAccounts of the users to be purged
             2. a set of uwnetids of the users to be purged
    """
    user_records = []  # store in a list
    user_set = set()  # store in a set
    total_notified_users = 0
    total_notify_err = 0

    email_address_domain = get_email_address_domain()
    path = get_file_path(filename='accounts1.csv')
    reader = csv.reader(open(path, 'r', encoding='utf8'), delimiter=',')
    next(reader)
    for line in reader:
        try:
            if line[1].endswith(email_address_domain):
                created_at = str_to_datetime(line[4])
                last_visit = str_to_datetime(line[5])
                acc = UserAccount(
                    uwnetid=re.sub(
                        email_address_domain, "", line[1], flags=re.I),
                    created_at=created_at, last_visit=last_visit)

                if int(line[7]) > 420:
                    # Will be purged in this run
                    user_records.append(acc)
                    user_set.add(acc.uwnetid)
                elif int(line[7]) > 360:
                    # Notify user before purging
                    if notify_inactive_users:
                        if send_acc_removal_email(acc.uwnetid):
                            total_notified_users += 1
                        else:
                            total_notify_err += 1
                else:
                    continue
        except Exception as ex:
            logger.error("{} in line: {}".format(ex, line))
    if notify_inactive_users:
        logger.info("Notified {} users".format(total_notified_users))
        logger.info(
            f"{total_notify_err} errors when sending notification email")

    return user_records, user_set
