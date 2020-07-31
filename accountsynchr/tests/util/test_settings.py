from django.test import TestCase
from django.conf import settings
from accountsynchr.util.settings import (
    get_csv_file_path, get_email_address_domain, get_user_email_sender,
    get_next_purge_date, get_cronjob_sender)


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

    def test_get_next_purge_date(self):
        with self.settings(PURGE_DATE='Jun 2, 2020'):
            self.assertEqual(get_next_purge_date(), "Jun 2, 2020")

    def test_get_cronjob_sender(self):
        with self.settings(CRONJOB_SENDER='none',
                           EMAIL_ADDRESS_DOMAIN='@test.edu'):
            self.assertEqual(get_cronjob_sender(), 'none@test.edu')
