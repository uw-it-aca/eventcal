from django.test import TestCase
from django.conf import settings
from accountsynchr.dao.inactive_accounts import (
    get_accounts_to_purge1, get_accounts_to_purge, get_file_path)


class TestInactiveAccounts(TestCase):

    def test_get_file_path(self):
        with self.settings(CSV_FILE_PATH='data'):
            self.assertEqual(get_file_path(), "data/accounts.csv")

    def test_get_accounts_to_purge(self):
        with self.settings(CSV_FILE_PATH=None,
                           EMAIL_ADDRESS_DOMAIN='@test.edu'):
            accounts_to_purge, user_set = get_accounts_to_purge(set())
            self.assertEqual(len(accounts_to_purge), 2)
            self.assertTrue('sdummys' in user_set)
            self.assertTrue('sdummyp' in user_set)
            self.assertEqual(accounts_to_purge[0].uwnetid, 'sdummys')
            self.assertEqual(accounts_to_purge[1].uwnetid, 'sdummyp')

    def test_get_accounts_to_purge1(self):
        with self.settings(CSV_FILE_PATH=None,
                           EMAIL_ADDRESS_DOMAIN='@test.edu'):
            accounts_to_purge, user_set = get_accounts_to_purge1(set())
            self.assertEqual(len(accounts_to_purge), 2)
            self.assertTrue('sdummys' in user_set)
            self.assertTrue('sdummyp' in user_set)
            self.assertEqual(accounts_to_purge[0].uwnetid, 'sdummys')
            self.assertEqual(accounts_to_purge[1].uwnetid, 'sdummyp')
