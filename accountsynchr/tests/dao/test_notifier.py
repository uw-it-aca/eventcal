from django.test import TestCase
from django.conf import settings
from accountsynchr.dao.notifier import (
    MESSAGE, SENDER, SUBJECT, send_acc_removal_email)


class TestNotification(TestCase):

    def test_acc_removal_email(self):
        self.assertEqual(len(MESSAGE), 422)
        self.assertEqual(SENDER, 'uweventcalweb@uw.edu')
        self.assertEqual(SUBJECT,
                         'Your Trumba Account Will Be Closed')
        self.assertTrue(send_acc_removal_email('sdummyp'))

    def test_error(self):
        with self.settings(EMAIL_BACKEND=''):
            self.assertFalse(send_acc_removal_email('sdummyp'))
