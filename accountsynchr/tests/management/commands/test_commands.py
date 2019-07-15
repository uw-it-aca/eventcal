from django.test import TestCase
from django.core.management import call_command


class TestCommands(TestCase):

    def test_add_account(self):
        call_command('add_account', 'sdummye', 'sdummye')

    def test_del_account(self):
        call_command('del_account', 'test10')

    def test_calendar(self):
        call_command('calendar')

    def test_cal_perms(self):
        call_command('cal_perms', 'bot')

    def test_find_user_groups(self):
        call_command('find_user_groups', 'dummye')

    def test_gws_trumba(self):
        call_command('gws_trumba')

    def test_trumba_gws(self):
        call_command('trumba_gws')
