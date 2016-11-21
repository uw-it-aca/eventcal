from django.test import TestCase
from django.conf import settings
from restclients.exceptions import DataFailureException
from accountsynchr.ucalgroup.group_manager import GroupManager
from accountsynchr.test import GWS_DAO_CLASS


class TestGroupManager(TestCase):

    def test_get_dict_normal_cases(self):
        with self.settings(RESTCLIENTS_GWS_DAO_CLASS=GWS_DAO_CLASS
                           ):
            campus_code = 'sea'
            gm = GroupManager()
            self.assertTrue(gm.exists(campus_code))
            result = gm._get_dict(campus_code)
            self.assertIsNotNone(result)
            self.assertEqual(gm.len(campus_code), 5)
            self.assertEqual(len(gm.get_group_names(campus_code)), 5)
            self.assertTrue(gm.has_group_name(campus_code,
                                              'u_eventcal_sea_1013649-editor'))
            self.assertTrue(gm.has_group_name(campus_code,
                                              'u_eventcal_sea_1036368-editor'))
            self.assertTrue(gm.has_group_name(campus_code,
                                              'u_eventcal_sea_1019930-editor'))
            self.assertTrue(gm.has_group_name(campus_code,
                                              'u_eventcal_sea_1036795-editor'))
            self.assertTrue(gm.has_group_name(campus_code,
                                              'u_eventcal_sea_1036589-editor'))

            name = 'u_eventcal_sea_1013649-editor'
            uwcal_group = gm.get_group_by_name(campus_code, name)
            self.assertEqual(uwcal_group.name, 'u_eventcal_sea_1013649-editor')
            self.assertEqual(uwcal_group.get_calendarid(), 1013649)
            self.assertEqual(uwcal_group.get_campus_code(), campus_code)
            self.assertTrue(uwcal_group.is_editor_group())

    def test_get_dict_empty_cases(self):
        with self.settings(RESTCLIENTS_GWS_DAO_CLASS=GWS_DAO_CLASS
                           ):
            campus_code = 'tac'
            gm = GroupManager()
            self.assertFalse(gm.exists(campus_code))

            result = gm._get_dict(campus_code)
            self.assertIsNotNone(result)
            self.assertEqual(gm.len(campus_code), 0)
