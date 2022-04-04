# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.test import TestCase
from django.conf import settings
from restclients_core.exceptions import DataFailureException
from accountsynchr.dao.gws import (
    Gws, _convert_to_gwsgroup, _convert_to_uwcalgroup)
from uw_gws.models import GroupReference
from accountsynchr.tests import fdao_gws_override


@fdao_gws_override
class TestGws(TestCase):

    def test_convert(self):
        groupr = GroupReference(uwregid="153f16f4fe6244bdb4be53559c9ed67b",
                                display_name="Bothell Calendar",
                                name="u_eventcal_bot_2-editor")
        uwcalgroup = _convert_to_uwcalgroup(groupr)
        self.assertEqual(uwcalgroup.calendar.to_json(),
                         {'calendarid': 2,
                          'campus': 'bot',
                          'name': 'Bothell Calendar',
                          'permissions': {}})
        self.assertEqual(uwcalgroup.gtype, 'editor')
        self.assertEqual(uwcalgroup.group_ref.name, groupr.name)

        gwsgroup = _convert_to_gwsgroup(uwcalgroup)
        self.assertEqual(gwsgroup.name, "u_eventcal_bot_2-editor")
        self.assertEqual(gwsgroup.display_name,
                         "Bothell Calendar calendar editor group")
        self.assertIsNotNone(gwsgroup.description)
        self.assertEqual(gwsgroup.admins[0].name, "u_eventcal_support")
        self.assertEqual(gwsgroup.updaters[0].name, "u_eventcal_bot_2-editor")
        self.assertIsNotNone(gwsgroup.json_data(is_put_req=True))

        groupr.name = "u_eventcal_bot_2-edit"
        self.assertIsNone(_convert_to_uwcalgroup(groupr))

    def test_get_campus_groups(self):
        gws = Gws()
        self.assertIsNone(gws.get_campus_groups('s'))

        grs = gws.get_campus_groups('bot')
        self.assertEqual(len(grs), 2)
        self.assertEqual(len(grs['editor']), 2)
        self.assertEqual(len(grs['showon']), 2)
        self.assertEqual(len(grs['editor'].keys()), 2)
        self.assertEqual(len(grs['showon'].values()), 2)

        g = grs['editor']["u_eventcal_bot_2-editor"]
        cal_json_2 = {'calendarid': 2,
                      'campus': 'bot',
                      'name': 'Bothell Campus Calendar',
                      'permissions': {}}
        self.assertEqual(g.calendar.to_json(), cal_json_2)
        self.assertEqual(g.gtype, 'editor')
        self.assertEqual(g.group_ref.name, "u_eventcal_bot_2-editor")

        self.assertEqual(len(g.members), 2)
        self.assertEqual(g.members[0].json_data(),
                         {'id': 'dummyp',
                          'mtype': 'direct',
                          'source': None,
                          'type': 'uwnetid'})

        self.assertEqual(g.members[1].json_data(),
                         {'id': 'dummye',
                          'mtype': 'direct',
                          'source': None,
                          'type': 'uwnetid'})

        g = grs['editor']["u_eventcal_bot_211-editor"]
        cal_json_211 = {'calendarid': 211,
                        'campus': 'bot',
                        'name': 'Bothell Campus >> Academic Calendars',
                        'permissions': {}}
        self.assertEqual(g.calendar.to_json(), cal_json_211)

        self.assertEqual(len(g.members), 1)
        self.assertEqual(g.members[0].json_data(),
                         {'id': 'dummys',
                          'mtype': 'direct',
                          'source': None,
                          'type': 'uwnetid'})
        self.assertEqual(len(grs['showon']), 2)
        g = grs['showon']["u_eventcal_bot_2-showon"]
        self.assertEqual(g.calendar.to_json(), cal_json_2)
        self.assertEqual(g.gtype, 'showon')

        g = grs['showon']["u_eventcal_bot_211-showon"]
        self.assertEqual(g.calendar.to_json(), cal_json_211)

        grs = gws.get_campus_groups('sea')
        self.assertEqual(len(grs), 2)

        grs = gws.get_campus_groups('tac')
        self.assertEqual(len(grs), 2)

        self.assertEqual(len(gws.all_editor_uwnetids), 6)
        self.assertEqual(len(gws.all_editors), 6)
        self.assertTrue(gws.is_existing_editor("dummyp"))
        self.assertTrue(gws.is_existing_editor("dummye"))
        self.assertTrue(gws.is_existing_editor("dummys"))
        self.assertTrue(gws.is_existing_editor("sdummye"))
        self.assertTrue(gws.is_existing_editor("sdummys"))
        self.assertTrue(gws.is_existing_editor("tdummye"))

    def test_put_groups(self):
        gws = Gws()
        grs = gws.get_campus_groups('bot')
        g = grs['editor']["u_eventcal_bot_2-editor"]

        gwsgroup = gws.put_group(g)
        self.assertEqual(gwsgroup.name, "u_eventcal_bot_2-editor")
        self.assertEqual(gwsgroup.display_name,
                         "Bothell Campus calendar editor group")

        self.assertIsNotNone(
            gws.put_group(grs['showon']["u_eventcal_bot_2-showon"]))
