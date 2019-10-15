from django.test import TestCase
from accountsynchr.gws_trumba import GwsToTrumba
from accountsynchr.user_purger import AccountPurger
from accountsynchr.tests import fdao_gws_override


@fdao_gws_override
class TestTrumbaToGws(TestCase):

    def test_group_member_purger(self):
        g_t = GwsToTrumba()
        g_t.sync()

        gmp = AccountPurger()
        gmp.gro_m = g_t.gro_m
        gmp.cal_per_m = g_t.cal_per_m

        gmp.sync()
        self.assertEqual(len(gmp.accounts_to_delete), 1)
        self.assertEqual(gmp.total_groups_purged, 2)
        self.assertEqual(gmp.total_accounts_deleted, 0)
        self.assertTrue(gmp.has_err())
