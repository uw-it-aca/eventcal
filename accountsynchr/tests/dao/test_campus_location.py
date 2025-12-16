# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.test import TestCase
from accountsynchr.dao.campus_location import (
    get_campus_locations_from_spacews)


class TestCampusLocation(TestCase):

    def test_get_campus_locations_from_spacews(self):
        locations = get_campus_locations_from_spacews()
        self.assertIsInstance(locations, list)
        self.assertGreater(len(locations), 0)
        loc = locations[1]
        self.assertEqual(loc.old_name, "")
        self.assertEqual(loc.old_code, "")
        self.assertIsNotNone(loc.space_obj)
        self.assertEqual(loc.space_obj.name, "")
        self.assertEqual(loc.space_obj.code, "")
