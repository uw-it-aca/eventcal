# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from datetime import datetime
from unittest.mock import patch
from django.test import TestCase
from uw_space import Facility, Facilities
from accountsynchr.dao.campus_location import (
    get_campus_locations_from_spacews)


class TestCampusLocation(TestCase):

    def test_get_campus_locations_from_spacews(self):
        with patch.object(Facilities, "search_by_code", spec=True) as mock:
            mock.return_value = [
                Facility(
                    code="NMEB",
                    latitude="47.653693",
                    longitude="-122.304747",
                    name="Mechanical Engineering Building",
                    number="1347",
                )
            ]
            locations = get_campus_locations_from_spacews()
            self.assertIsInstance(locations, list)
            self.assertEqual(len(locations), 281)
            loc = locations[1]
            self.assertEqual(loc.old_name, "1218 NE Campus Parkway")
            self.assertEqual(loc.old_code, "ELM-HALL")
            self.assertEqual(loc.space_obj.code, "NMEB")
            self.assertEqual(
                loc.space_obj.name, "Mechanical Engineering Building")
            self.assertEqual(loc.space_obj.latitude, "47.653693")
            self.assertEqual(loc.space_obj.longitude, "-122.304747")

            loc = locations[280]
            self.assertEqual(
                loc.old_name, "Women's Fastpitch Softball Building")
            self.assertEqual(loc.old_code, "WSB")
            self.assertEqual(loc.space_obj.code, "NMEB")
            self.assertEqual(
                loc.space_obj.name, "Mechanical Engineering Building")
            self.assertEqual(loc.space_obj.latitude, "47.653693")
            self.assertEqual(loc.space_obj.longitude, "-122.304747")
