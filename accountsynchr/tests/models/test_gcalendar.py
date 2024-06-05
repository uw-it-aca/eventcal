# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.test import TransactionTestCase
from uw_gws.models import GroupReference
from uw_trumba.models import TrumbaCalendar
from accountsynchr.models import GCalendar


class TestGCalendar(TransactionTestCase):

    def test_creatte_update(self):
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
