# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase
from django.conf import settings
from accountsynchr.gws_trumba import GwsToTrumba
from accountsynchr.user_purger import AccountPurger
from accountsynchr.tests import fdao_gws_override


@fdao_gws_override
class TestTrumbaToGws(TestCase):

    def test_group_member_purger(self):
        with self.settings(CSV_FILE_PATH=None,
                           EMAIL_ADDRESS_DOMAIN='@test.edu'):
            g_t = GwsToTrumba()
            g_t.sync()

            acc_pgr = AccountPurger()
            acc_pgr.gro_m = g_t.gro_m
            acc_pgr.cal_per_m = g_t.cal_per_m
            acc_pgr.set_accounts_to_purge()
            acc_pgr.sync()
            self.assertEqual(len(acc_pgr.accounts_to_delete), 2)
            self.assertEqual(acc_pgr.total_groups_purged, 2)
            self.assertEqual(acc_pgr.total_accounts_deleted, 1)
            self.assertTrue(acc_pgr.has_err())
