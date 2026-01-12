# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from unittest.mock import patch
from django.test import TestCase
from uw_space import Facility, Facilities
from accountsynchr.dao.campus_location import (
    CampusLocation, tidy_name,
    get_campus_locations_from_spacews,
    parse_campus_location_title
)


class TestCampusLocation(TestCase):
    def test_parse_campus_location_title(self):
        name, code = parse_campus_location_title(
            "Union Bay Natural Area"
        )
        self.assertEqual(name, "Union Bay Natural Area")
        self.assertEqual(code, "")

        name, code = parse_campus_location_title(
            "Women's Fastpitch Softball Building (WSB)")
        self.assertEqual(name, "Women's Fastpitch Softball Building")
        self.assertEqual(code, "WSB")

        name, code = parse_campus_location_title(
            "The Liberal Arts Quadrangle - The Quad (LNDMK-1)"
        )
        self.assertEqual(
            name, "The Liberal Arts Quadrangle - The Quad (LNDMK-1)")
        self.assertEqual(code, "")

        name, code = parse_campus_location_title(
            "North Physics Laboratory (Van De Graaff Accelerator) (npv)"
        )
        self.assertEqual(
            name, "North Physics Laboratory (Van De Graaff Accelerator)")
        self.assertEqual(code, "npv")

    def test_find_space_obj(self):
        value = {
                "city": "Seattle",
                "code": "MDR",
                "last_updated": "2022-09-22 12:49:38-07:53",
                "latitude": 47.6601320001,
                "longitude": -122.305391,
                "name": "Madrona Hall",
                "number": "6471",
                "post_code": "98195",
                "site": "Seattle Main Campus",
                "state": "WA",
                "status": "A",
                "street": "4320 Little Canoe Channel NE",
                "type": "Building"
            }
        cl = CampusLocation("1", "MDR")
        fac = cl.space_obj
        self.assertEqual(fac.json_data(), value)

        cl = CampusLocation("1", "MDR1")
        fac = cl.space_obj
        self.assertIsNone(fac)

        cl2 = CampusLocation("Allen_Library", "")
        fac = cl2.space_obj
        self.assertIsNotNone(fac.json_data())

        cl3 = CampusLocation("4320 Little Canoe Channel NE", "")
        fac = cl3.space_obj
        self.assertIsNone(fac)

        cl3 = CampusLocation("668 NE Northlake Way", "")
        fac = cl3.space_obj
        self.assertIsNotNone(fac)

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
            self.assertTrue(len(locations) > 250)

            loc = locations[len(locations) - 1]
            self.assertEqual(
                loc.old_name, "Women's Fastpitch Softball Building")
            self.assertEqual(loc.old_code, "WSB")
            self.assertEqual(loc.space_obj.code, "NMEB")
            self.assertEqual(
                loc.space_obj.name, "Mechanical Engineering Building")
            self.assertEqual(loc.space_obj.latitude, "47.653693")
            self.assertEqual(loc.space_obj.longitude, "-122.304747")

    def test_tidy_name(self):
        self.assertEqual(tidy_name(""), "")
        self.assertEqual(
            tidy_name("4522 University Way NE (**DUPLICATE OF 1088**)"),
            "4522 University Way NE"
        )
        self.assertEqual(
            tidy_name("SLU D Building (Brotman)"),
            "SLU D Building (Brotman)"
        )
