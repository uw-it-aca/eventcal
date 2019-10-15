from django.test import TestCase
from django.conf import settings
from accountsynchr.dao.dead_accounts import (
    get_accounts_to_purge, get_file_path)


class TestDeadAccounts(TestCase):

    def test_get_file_path(self):
        with self.settings(CSV_FILE_PATH='data'):
            self.assertEqual(get_file_path(), "data/acounts.csv")

    def test_get_accounts_to_purge(self):
        with self.settings(CSV_FILE_PATH=None):
            accounts_to_purge, user_set = get_accounts_to_purge()
            self.assertEqual(len(accounts_to_purge), 1)
            self.assertTrue('sdummys' in user_set)
            self.assertEqual(accounts_to_purge[0].uwnetid, 'sdummys')
