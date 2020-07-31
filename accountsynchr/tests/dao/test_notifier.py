from datetime import datetime
from django.test import TestCase
from django.conf import settings
from accountsynchr.dao.notifier import (
    send_acc_removal_email, get_next_purge_date)


class TestNotification(TestCase):
    def test_get_next_purge_date(self):
        now = datetime(2020, 1, 1, 0, 0, 1)
        self.assertEqual(str(get_next_purge_date(now)), "2020-02-01")
        now = datetime(2020, 2, 1, 0, 0, 1)
        self.assertEqual(str(get_next_purge_date(now)), "2020-03-01")
        now = datetime(2020, 12, 1, 0, 0, 1)
        self.assertEqual(str(get_next_purge_date(now)), "2021-01-01")

    def test_acc_removal_email(self):
        with self.settings(EMAIL_BACKEND='saferecipient.EmailBackend',
                           SAFE_EMAIL_RECIPIENT='none',
                           EMAIL_ADDRESS_DOMAIN='@uw.edu',
                           EMAIL_SENDER='none@uw.edu',
                           PURGE_DATE='Jun 1, 2020'):
            self.assertFalse(send_acc_removal_email('sdummyp'))
