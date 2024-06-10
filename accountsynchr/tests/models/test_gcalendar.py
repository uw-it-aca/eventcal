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
                calendarid=n, campus="bot", name="Bothell" + str(n))
            GCalendar.create(trumba_cal)

        records = GCalendar.objects.all()
        self.assertEqual(len(records), 6)

        self.assertTrue(GCalendar.exists(trumba_cal))
        cal1 = GCalendar.objects.get(
            campus="bot", name="Bothell1")
        self.assertEqual(hash(cal1), 1)
        cal2 = GCalendar.objects.get(
            campus="bot", name="Bothell2")
        self.assertTrue(cal1 < cal2)
        self.assertFalse(cal1 == cal2)
        res = cal1.__lt__(None)
        self.assertEqual(res, NotImplemented)

        obj = GCalendar.update(TrumbaCalendar(
            calendarid=1, campus="bot", name="Bot1"))
        self.assertEqual(
            obj.to_json(),
            {"calendarid": 1, "campus": "bot", "name": "Bot1"})
        self.assertIsNotNone(str(obj))
