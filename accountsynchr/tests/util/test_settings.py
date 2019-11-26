from django.test import TestCase
from django.conf import settings
from accountsynchr.util.settings import (
    get_csv_file_path, get_email_address_domain, get_email_sender,
    get_email_message, get_email_subject)


class TestSettings(TestCase):

    def test_get_csv_file_path(self):
        with self.settings(CSV_FILE_PATH='data'):
            self.assertEqual(get_csv_file_path(), "data")

    def test_get_email_address_domain(self):
        with self.settings(EMAIL_ADDRESS_DOMAIN='@test.edu'):
            self.assertEqual(get_email_address_domain(),
                             "@test.edu")

    def test_get_email_sender(self):
        with self.settings(EMAIL_SENDER='eventcal@test.edu'):
            self.assertEqual(get_email_sender(),
                             "eventcal@test.edu")

    def test_get_email_message(self):
        with self.settings(PURGE_EMAIL_MESSAGE='Body'):
            self.assertEqual(get_email_message(),
                             "Body")

    def test_get_email_subject(self):
        with self.settings(PURGE_EMAIL_SUBJECT='Subject'):
            self.assertEqual(get_email_subject(),
                             "Subject")
