import logging
import csv
import os
import re
from dateutil.parser import parse
from datetime import date, datetime, timedelta
from accountsynchr.util.settings import get_csv_file_path
from accountsynchr.models import UserAccount
from accountsynchr.dao.notifier import send_acc_removal_email

logger = logging.getLogger(__name__)


def get_file_path():
    file_path = get_csv_file_path()
    if file_path is None:
        file_path = os.path.join(os.path.dirname(__file__), '..', 'data')
    return os.path.join(file_path, 'accounts.csv')


def get_accounts_to_purge(existing_group_member_set,
                          notify_inactive_users=False):
    """
    Also email users to be purged in the next month.
    returns: 1. a list of UserAccounts of the users to be purged
             2. a set of uwnetids of the users to be purged
    """
    notify_timedelta = datetime.now() - timedelta(days=365)
    purge_timedelta = notify_timedelta - timedelta(days=30)
    total_notified_users = 0
    total_notify_err = 0

    path = get_file_path()
    user_records = []
    user_set = set()
    reader = csv.reader(open(path, 'r', encoding='utf8'), delimiter=',')
    next(reader)
    for line in reader:
        try:
            if line[2].endswith("@uw.edu"):
                last_visit = str_to_datetime(line[4])
                acc = UserAccount(uwnetid=_extract_uwnetid(line[2]),
                                  last_visit=last_visit)
                if last_visit is not None:

                    if last_visit < purge_timedelta:
                        # Will be purged in this run
                        user_records.append(acc)
                        user_set.add(acc.uwnetid)

                    elif last_visit < notify_timedelta:
                        # Notify user before purging
                        if notify_inactive_users:
                            if send_acc_removal_email(acc.uwnetid):
                                total_notified_users += 1
                            else:
                                total_notify_err += 1
                else:
                    # Has never accessed Trumba
                    if acc.uwnetid not in existing_group_member_set:
                        # Not in any editor group, purged
                        user_records.append(acc)
                        user_set.add(acc.uwnetid)
        except Exception as ex:
            logger.error("{} in line: {}".format(str(ex), line))
        if notify_inactive_users:
            logger.info("Notified {} users".format(total_notified_users))
            logger.info("{} errors when sending notification email".format(
                    total_notified_users))
    return user_records, user_set


def str_to_datetime(s):
    return parse(s) if (s is not None and len(s)) else None


def _extract_uwnetid(email):
    return re.sub("@uw.edu", "", email, flags=re.I).lower()
