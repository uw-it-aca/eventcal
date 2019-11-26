from django.test import TestCase
from django.conf import settings
from accountsynchr.dao.notifier import send_acc_removal_email


class TestNotification(TestCase):

    def test_acc_removal_email(self):
        with self.settings(EMAIL_BACKEND='saferecipient.EmailBackend',
                           SAFE_EMAIL_RECIPIENT='eventcal@test.edu',
                           EMAIL_ADDRESS_DOMAIN='@test.edu',
                           EMAIL_SENDER='eventcal@test.edu',
                           PURGE_EMAIL_MESSAGE='Body',
                           PURGE_EMAIL_SUBJECT='Subject'):
            self.assertFalse(send_acc_removal_email('sdummyp'))
