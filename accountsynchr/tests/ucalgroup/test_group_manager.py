from django.test import TestCase
from django.conf import settings
from uw_trumba.models import TrumbaCalendar
from accountsynchr.ucalgroup.group_manager import GroupManager
from accountsynchr.tests import fdao_gws_override


@fdao_gws_override
class TestGroupManager(TestCase):

    def test_group_manager(self):
        gm = GroupManager()

        self.assertEqual(len(gm.get_all_editors()), 6)
        self.assertEqual(len(gm.get_campus_editor_groups('bot')), 2)
        self.assertEqual(len(gm.get_campus_showon_groups('bot')), 2)
        self.assertEqual(len(gm.get_campus_editor_groups('sea')), 3)
        self.assertEqual(len(gm.get_campus_showon_groups('tac')), 1)

        cal1 = TrumbaCalendar(calendarid=2,
                              campus='bot',
                              name='Bothell Campus')
        cal2 = TrumbaCalendar(calendarid=211,
                              name='Bothell Campus >> Academic Calendars',
                              campus='bot')
        cal3 = TrumbaCalendar(
            calendarid=2111,
            name='Bothell Campus >> Academic Calendars >> Holidays',
            campus='bot')

        self.assertTrue(gm.has_editor_group(cal1))
        self.assertTrue(gm.has_editor_group(cal2))
        self.assertFalse(gm.has_editor_group(cal3))
        self.assertTrue(gm.has_showon_group(cal1))
        self.assertTrue(gm.has_showon_group(cal2))
        self.assertFalse(gm.has_showon_group(cal3))

        egroup = gm.get_editor_group(cal2)
        self.assertTrue(egroup.same_name(cal2))
        sgroup = gm.get_showon_group(cal2)
        self.assertTrue(sgroup.same_name(cal2))
        self.assertIsNotNone(gm.put_editor_group(cal2))
        self.assertIsNotNone(gm.put_showon_group(cal2))

        egroup = gm.get_editor_group(cal1)
        self.assertFalse(egroup.same_name(cal1))
        uwcal_group = gm.put_editor_group(cal1)
        self.assertEqual(
            uwcal_group.to_json(),
            {'calendar': {
                    'calendarid': 2,
                    'campus': 'bot',
                    'name': 'Bothell Campus',
                    'permissions': {}},
             'group_ref': {
                    'displayName': 'Bothell Campus calendar editor group',
                    'id': 'u_eventcal_bot_2-editor',
                    'regid': '806cdfb7c41843b6833e5c860b0dc615'},
             'gtype': 'editor',
             'members': [{'id': 'dummyp',
                          'mtype': 'direct',
                          'source': None,
                          'type': 'uwnetid'},
                         {'id': 'dummye',
                          'mtype': 'direct',
                          'source': None,
                          'type': 'uwnetid'}]})

        uwcal_group = gm.put_showon_group(cal1)
        # self.maxDiff = None
        self.assertEqual(
            uwcal_group.to_json(),
            {'calendar': {'calendarid': 2,
                          'campus': 'bot',
                          'name': 'Bothell Campus',
                          'permissions': {}},
             'group_ref': {
                 'displayName': 'Bothell Campus calendar showon group',
                 'id': 'u_eventcal_bot_2-showon',
                 'regid': '806cdfb7c41843b6833e5c860b0dc615'},
             'gtype': 'showon',
             'members': [{'id': 'dummys',
                          'mtype': 'direct',
                          'source': None,
                          'type': 'uwnetid'}]})

        cal1 = TrumbaCalendar(calendarid=1,
                              campus='sea',
                              name="Seattle Campus")
        cal1_editor_group = gm.get_editor_group(cal1)
        self.assertIsNotNone(cal1_editor_group)
        self.assertTrue(cal1_editor_group.same_name(cal1))
        ret_uwcal_group = gm.put_editor_group(cal1)
        self.assertTrue(cal1_editor_group == ret_uwcal_group)

        cal1_showon_group = gm.get_showon_group(cal1)
        self.assertIsNotNone(cal1_showon_group)
        self.assertTrue(cal1_showon_group.same_name(cal1))
        ret_uwcal_group = gm.put_showon_group(cal1)
        self.assertTrue(cal1_showon_group == ret_uwcal_group)
