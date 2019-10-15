import logging
import csv
import os
import re
from dateutil.parser import parse
from datetime import date, datetime, timedelta
from accountsynchr.util.settings import get_csv_file_path
from accountsynchr.models import UserAccount

logger = logging.getLogger(__name__)


def get_file_path():
    file_path = get_csv_file_path()
    if file_path is None:
        file_path = os.path.join(os.path.dirname(__file__), '..', 'data')
    return os.path.join(file_path, 'accounts.csv')


def get_accounts_to_purge(existing_group_member_set):
    """
    returns: 1. a list of UserAccount
             2. a set of uwnetids
    """
    path = get_file_path()
    one_year_ago = datetime.now() + timedelta(days=365)

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
                    # check last_visit
                    if last_visit < one_year_ago:
                        user_records.append(acc)
                        user_set.add(acc.uwnetid)
                else:
                    # has never visited
                    if acc.uwnetid not in existing_group_member_set:
                        user_records.append(acc)
                        user_set.add(acc.uwnetid)
        except Exception as ex:
            logger.error("{} in line: {}".format(str(ex), line))

    return user_records, user_set


def str_to_datetime(s):
    return parse(s) if (s is not None and len(s)) else None


def _extract_uwnetid(email):
    return re.sub("@uw.edu", "", email, flags=re.I).lower()
