from django.test import TestCase
from accountsynchr.trumba_gws import TrumbaToGws
from accountsynchr.tests import fdao_gws_override


@fdao_gws_override
class TestTrumbaToGws(TestCase):

    def test_group_manager(self):
        tg = TrumbaToGws()
        tg.sync()
        self.assertEqual(tg.ttl_editor_grps_synced, 6)
        self.assertEqual(tg.ttl_showon_grp_synced, 6)
        self.assertEqual(tg.del_editor_perm_counts, 2)
        self.assertEqual(tg.del_showon_perm_counts, 2)
        self.assertFalse(tg.has_err())
