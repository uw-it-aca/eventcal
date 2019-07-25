from django.test import TestCase
from uw_gws.models import GroupReference
from uw_trumba.models import TrumbaCalendar
from accountsynchr.models import (
    UwcalGroup, new_editor_group, new_showon_group, get_cal_name)


class TestModels(TestCase):

    def test_uwcalgroup(self):
        trumba_cal = TrumbaCalendar(calendarid=2, campus="bot")
        editor_gr = new_editor_group(trumba_cal)
        editor_gr.set_calendar_name("Bothell Campus")
        self.assertEqual(trumba_cal.name, "Bothell Campus")
        showon_gr = new_showon_group(trumba_cal)

        # UwcalGroup methods
        self.assertEqual(editor_gr.get_calendarid(), 2)
        self.assertEqual(editor_gr.get_campus_code(), "bot")
        self.assertFalse(editor_gr.has_group_ref())
        self.assertIsNone(editor_gr.get_regid())
        self.assertEqual(editor_gr.get_group_id(), "u_eventcal_bot_2-editor")
        self.assertEqual(editor_gr.get_group_name(),
                         "u_eventcal_bot_2-editor")
        self.assertEqual(editor_gr.get_group_admin(), "u_eventcal_support")
        self.assertIsNotNone(editor_gr.get_group_desc())
        self.assertEqual(editor_gr.get_group_title(),
                         "Bothell Campus calendar editor group")
        self.assertEqual(editor_gr.get_member_manager(),
                         "u_eventcal_bot_2-editor")

        self.assertTrue(editor_gr.is_editor_group())
        self.assertFalse(showon_gr.is_editor_group())
        self.assertFalse(editor_gr.is_showon_group())
        self.assertTrue(showon_gr.is_showon_group())

        # group_ref is None
        self.assertFalse(editor_gr.same_name(trumba_cal))
        self.assertFalse(showon_gr.same_name(trumba_cal))

        self.assertEqual(editor_gr.to_json(),
                         {'calendar': {'calendarid': 2,
                                       'campus': 'bot',
                                       'name': 'Bothell Campus',
                                       'permissions': {}},
                          'group_ref': None,
                          'gtype': 'editor',
                          'members': []})

        editor_gr.group_ref = GroupReference()
        editor_gr.group_ref.name = "u_eventcal_bot_2-editor"
        editor_gr.group_ref.display_name = 'Bothell Campus'

        showon_gr.group_ref = GroupReference()
        showon_gr.group_ref.name = "u_eventcal_bot_2-showon"
        showon_gr.group_ref.display_name = \
            'Bothell Campus calendar showon group'

        self.assertTrue(editor_gr.same_name(trumba_cal))
        self.assertTrue(showon_gr.same_name(trumba_cal))

        self.assertTrue(editor_gr == editor_gr)
        self.assertFalse(editor_gr == showon_gr)

        self.assertEqual(editor_gr.to_json(),
                         {'calendar': {'calendarid': 2,
                                       'campus': 'bot',
                                       'name': 'Bothell Campus',
                                       'permissions': {}},
                          'group_ref': {'displayName': 'Bothell Campus',
                                        'id': 'u_eventcal_bot_2-editor',
                                        'regid': ''},
                          'gtype': 'editor',
                          'members': []})
        self.assertIsNotNone(str(editor_gr))

    def test_get_cal_name(self):
        self.assertEqual(get_cal_name("UW Tacoma Campus Events"),
                         "UW Tacoma Campus Events")
        self.assertEqual(get_cal_name("Tacoma Campus calendar editor group"),
                         "Tacoma Campus")
        self.assertEqual(get_cal_name("Tacoma Campus calendar showon group"),
                         "Tacoma Campus")
        self.assertEqual(get_cal_name(
                "Foster School of Business >> Mktg & Int'l Business " +
                "calendar showon group"),
                         "Foster School of Business >> Mktg & Int'l Business")
        self.assertEqual(get_cal_name(
                "Athletics >> UW Women's Basketball calendar editor group"),
                "Athletics >> UW Women's Basketball")
