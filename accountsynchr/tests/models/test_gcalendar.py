# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.test import TransactionTestCase
from uw_gws.models import GroupReference
from uw_trumba.models import TrumbaCalendar
from accountsynchr.models import (
    GCalendar, new_editor_group, new_showon_group, get_cal_name)


class TestModels(TransactionTestCase):

    def test_uwcalgroup(self):
        for n in range(6):
            trumba_cal = TrumbaCalendar(
                calendarid=n + 1, campus="bot", name="Bothell" + str(n))
            GCalendar.create(trumba_cal)

        records = GCalendar.objects.all()
        self.assertEqual(len(records), 6)
        
        self.assertTrue(GCalendar.exists(trumba_cal))

        obj = GCalendar.update(TrumbaCalendar(
            calendarid=1, campus="bot", name="Bot1"))
        self.assertEqual(
            obj.to_json(),
            {"calendarid": 1, "campus": "bot", "name": "Bot1"})
        self.assertIsNotNone(str(obj))
