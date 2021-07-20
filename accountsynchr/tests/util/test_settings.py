# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase
from django.conf import settings
from accountsynchr.util.settings import (
    get_csv_file_path, get_email_address_domain, get_user_email_sender,
    get_cronjob_sender)


class TestSettings(TestCase):

    def test_get_csv_file_path(self):
        with self.settings(CSV_FILE_PATH='data'):
            self.assertEqual(get_csv_file_path(), "data")

    def test_get_email_address_domain(self):
        with self.settings(EMAIL_ADDRESS_DOMAIN='@test.edu'):
            self.assertEqual(get_email_address_domain(), "@test.edu")

    def test_get_user_email_sender(self):
        with self.settings(EMAIL_ADDRESS_DOMAIN='@test.edu',
                           EMAIL_SENDER='eventc'):
            self.assertEqual(get_user_email_sender(), "eventc@test.edu")

    def test_get_cronjob_sender(self):
        with self.settings(CRONJOB_SENDER='none',
                           EMAIL_ADDRESS_DOMAIN='@test.edu'):
            self.assertEqual(get_cronjob_sender(), 'none@test.edu')
