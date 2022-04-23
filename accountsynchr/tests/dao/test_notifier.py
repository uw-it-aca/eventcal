# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from datetime import datetime
from django.test import TestCase
from django.conf import settings
from accountsynchr.dao.notifier import (
    send_acc_removal_email, get_next_purge_date)


class TestNotification(TestCase):
    def test_get_next_purge_date(self):
        now = datetime(2020, 1, 1, 0, 0, 1)
        self.assertEqual(str(get_next_purge_date(now)), "Feb 1, 2020")
        now = datetime(2020, 2, 1, 0, 0, 1)
        self.assertEqual(str(get_next_purge_date(now)), "Mar 1, 2020")
        now = datetime(2020, 12, 1, 0, 0, 1)
        self.assertEqual(str(get_next_purge_date(now)), "Jan 1, 2021")

    def test_acc_removal_email(self):
        with self.settings(EMAIL_BACKEND='saferecipient.EmailBackend',
                           SAFE_EMAIL_RECIPIENT='none',
                           EMAIL_ADDRESS_DOMAIN='@uw.edu',
                           EMAIL_SENDER='none@uw.edu',
                           PURGE_DATE='Jun 1, 2020'):
            self.assertFalse(send_acc_removal_email('sdummyp'))
