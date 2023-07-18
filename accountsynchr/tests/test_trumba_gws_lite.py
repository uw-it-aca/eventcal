# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.test import TransactionTestCase
from accountsynchr.models.gcalendar import GCalendar
from accountsynchr.trumba_gws_lite import TrumbaGwsLite
from accountsynchr.tests import fdao_gws_override


@fdao_gws_override
class TestTrumbaGwsLite(TransactionTestCase):

    def test_group_manager(self):
        tg = TrumbaGwsLite()
        tg.sync()
        self.assertEqual(tg.ttl_editor_grps_synced, 2)
        self.assertEqual(tg.ttl_showon_grp_synced, 2)
        self.assertTrue(tg.has_err())
        self.assertTrue(len(tg.get_error_report()) > 0)
        records = GCalendar.objects.all()
        self.assertEqual(len(records), 6)
