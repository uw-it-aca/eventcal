from django.test import TestCase
from django.conf import settings
from accountsynchr.util.settings import get_csv_file_path


class TestSettings(TestCase):

    def test_get_csv_file_path(self):
        with self.settings(CSV_FILE_PATH='data'):
            self.assertEqual(get_csv_file_path(), "data")
