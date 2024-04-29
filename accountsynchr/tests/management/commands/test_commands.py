# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.test import TransactionTestCase
from django.core.management import call_command
from accountsynchr.models.gcalendar import GCalendar


class TestCommands(TransactionTestCase):

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
        call_command('purge_accounts')
        call_command('acc_rm_notify', 'sdummyp')

    def test_load_gcal(self):
        call_command('load_gcal')
        records = GCalendar.objects.all()
        self.assertEqual(len(records), 6)

    def test_trumba_gcal_gws(self):
        call_command('trumba_gcal_gws')
        records = GCalendar.objects.all()
        self.assertEqual(len(records), 2)
