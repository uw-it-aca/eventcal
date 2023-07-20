# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.test import TransactionTestCase
from unittest.mock import patch
from uw_trumba.models import TrumbaCalendar
from accountsynchr.models.gcalendar import GCalendar
from accountsynchr.dao.gws import Gws
from accountsynchr.trumba_gws_lite import TrumbaGwsLite
from accountsynchr.tests import fdao_gws_override


@fdao_gws_override
class TestTrumbaGwsLite(TransactionTestCase):

    @patch.object(Gws, 'put_group')
    def test_sync_success(self, mock):
        GCalendar.create(
            TrumbaCalendar(calendarid=1, campus="sea", name="Seattle"))
        mock.return_value = 1
        tg = TrumbaGwsLite()
        tg.sync()
        self.assertEqual(tg.ttl_editor_grps_synced, 6)
        self.assertEqual(tg.ttl_showon_grp_synced, 6)
        self.assertEqual(tg.ttl_gcal_updated, 6)
        self.assertFalse(tg.has_err())
        self.assertTrue(len(tg.get_error_report()) == 0)
        records = GCalendar.objects.all()
        self.assertEqual(len(records), 6)
        self.assertEqual(records[0].name, "Seattle Campus")

    @patch.object(TrumbaGwsLite, 'put_editor_group')
    def test_sync_showon_failure(self, mock):
        mock.return_value = 1
        tg = TrumbaGwsLite()
        tg.sync()
        self.assertEqual(tg.ttl_editor_grps_synced, 6)
        self.assertEqual(tg.ttl_showon_grp_synced, 2)
        self.assertEqual(tg.ttl_gcal_updated, 2)
        self.assertTrue(tg.has_err())
        self.assertTrue(len(tg.get_error_report()) > 0)
        records = GCalendar.objects.all()
        self.assertEqual(len(records), 2)
