# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from datetime import datetime
from django.test import TestCase
from unittest.mock import patch
from accountsynchr.dao.inactive_accounts import (
    get_accounts_to_purge1, get_accounts_to_purge, get_file_path)


class TestInactiveAccounts(TestCase):

    def test_get_file_path(self):
        with self.settings(CSV_FILE_PATH='data'):
            self.assertEqual(get_file_path(), "data/accounts.csv")

    @patch('accountsynchr.dao.notifier.send_acc_removal_email', spec=True)
    def test_get_accounts_to_purge(self, mock):
        with self.settings(CSV_FILE_PATH=None,
                           EMAIL_ADDRESS_DOMAIN='@test.edu'):
            mock.return_value = True
            accounts_to_purge, user_set = get_accounts_to_purge(
                set(), notify_inactive_users=True,
                dtnow = datetime(2014, 8, 8))
            self.assertEqual(len(accounts_to_purge), 2)
            self.assertTrue('sdummys' in user_set)
            self.assertTrue('sdummyp' in user_set)
            self.assertEqual(accounts_to_purge[0].uwnetid, 'sdummyp')
            self.assertEqual(accounts_to_purge[1].uwnetid, 'sdummys')

    @patch('accountsynchr.dao.notifier.send_acc_removal_email', spec=True)
    def test_get_accounts_to_purge1(self, mock):
        with self.settings(CSV_FILE_PATH=None,
                           EMAIL_ADDRESS_DOMAIN='@test.edu'):
            mock.return_value = False
            accounts_to_purge, user_set = get_accounts_to_purge1(
                set(), notify_inactive_users=True)
            self.assertEqual(len(accounts_to_purge), 2)
            self.assertTrue('sdummys' in user_set)
            self.assertTrue('sdummyp' in user_set)
            self.assertEqual(accounts_to_purge[0].uwnetid, 'sdummys')
            self.assertEqual(accounts_to_purge[1].uwnetid, 'sdummyp')

    @patch('accountsynchr.dao.notifier.send_acc_removal_email', spec=True)
    def test_get_accounts_to_purge_err(self, mock):
        with self.settings(CSV_FILE_PATH=None,
                           EMAIL_ADDRESS_DOMAIN='@test.edu'):
            mock.side_effect = Exception
            accounts_to_purge, user_set = get_accounts_to_purge1(
                set(), notify_inactive_users=True)
            self.assertEqual(len(accounts_to_purge), 2)
            self.assertTrue('sdummys' in user_set)
