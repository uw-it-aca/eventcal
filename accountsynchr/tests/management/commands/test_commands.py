from django.test import TestCase
from django.core.management import call_command


class TestCommands(TestCase):

    def test_accounts_vs_members(self):
        call_command('accounts_vs_members')

    def test_add_account(self):
        call_command('add_account', 'sdummye', 'sdummye')

    def test_calendar(self):
        call_command('cal_stats')

    def test_cal_perms(self):
        call_command('cal_perms', 'bot')

    def test_group_stats(self):
        call_command('group_stats')

    def test_find_user_groups(self):
        call_command('find_user_groups', 'dummye')
        call_command('find_user_groups', 'dummys')

    def test_gws_trumba(self):
        call_command('gws_trumba')

    def test_trumba_gws(self):
        call_command('trumba_gws')

    def test_purge_accounts(self):
        with self.settings(EMAIL_BACKEND='saferecipient.EmailBackend',
                           SAFE_EMAIL_RECIPIENT='none',
                           EMAIL_ADDRESS_DOMAIN='@uw.edu',
                           EMAIL_SENDER='none@uw.edu',
                           PURGE_DATE='Aug 30, 2020'):
            call_command('purge_accounts')

    def test_acc_rm_notify(self):
        with self.settings(EMAIL_BACKEND='saferecipient.EmailBackend',
                           SAFE_EMAIL_RECIPIENT='none',
                           EMAIL_ADDRESS_DOMAIN='@uw.edu',
                           EMAIL_SENDER='none@uw.edu',
                           PURGE_DATE='Aug 30, 2020'):
            call_command('acc_rm_notify', 'sdummyp')
