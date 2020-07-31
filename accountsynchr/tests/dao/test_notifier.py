from django.test import TestCase
from django.conf import settings
from accountsynchr.dao.notifier import send_acc_removal_email


class TestNotification(TestCase):

    def test_acc_removal_email(self):
        with self.settings(EMAIL_BACKEND='saferecipient.EmailBackend',
                           SAFE_EMAIL_RECIPIENT='none',
                           EMAIL_ADDRESS_DOMAIN='@uw.edu',
                           EMAIL_SENDER='none@uw.edu',
                           PURGE_DATE='Jun 1, 2020'):
            self.assertFalse(send_acc_removal_email('sdummyp'))
