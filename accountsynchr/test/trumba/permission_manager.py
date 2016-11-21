from django.test import TestCase
from django.conf import settings
from restclients.exceptions import DataFailureException
from restclients.models.trumba import TrumbaCalendar
from accountsynchr.trumba.permission_manager import PermissionManager
from accountsynchr.test import BOT_DAO_CLASS, SEA_DAO_CLASS, TAC_DAO_CLASS


class TestPermissionManager(TestCase):

    def test_get_all_accounts(self):
        with self.settings(RESTCLIENTS_TRUMBA_BOT_DAO_CLASS=BOT_DAO_CLASS,
                           RESTCLIENTS_TRUMBA_SEA_DAO_CLASS=SEA_DAO_CLASS,
                           RESTCLIENTS_TRUMBA_TAC_DAO_CLASS=TAC_DAO_CLASS):

            per_m = PermissionManager()
            users = per_m.get_all_accounts()
            self.assertIsNotNone(users)
            self.assertEqual(len(users), 3)
            self.assertTrue('dummyp' in users)
            self.assertTrue('dummye' in users)
            self.assertTrue('dummys' in users)

            sea_cal = TrumbaCalendar(calendarid=1,
                                     campus='sea',
                                     name='Seattle calendar')
            self.assertTrue(per_m.has_editor(sea_cal))
            self.assertTrue(per_m.has_showon(sea_cal))
            self.assertTrue(per_m.exists(sea_cal))
            edit_perms = per_m.get_editor_permissions(sea_cal)
            self.assertEqual(len(edit_perms), 2)
            self.assertEqual(len(per_m.get_showon_permissions(sea_cal)), 1)
            self.assertTrue(per_m.is_editor(sea_cal, 'dummye'))
            self.assertTrue(per_m.is_editor(sea_cal, 'dummyp'))
            self.assertTrue(per_m.is_showon(sea_cal, 'dummys'))

            editor1 = edit_perms[0]
            self.assertTrue(editor1.is_publish())
            self.assertTrue(editor1.is_edit())
            editor2 = edit_perms[1]
            self.assertFalse(editor2.is_publish())
            self.assertTrue(editor2.is_edit())
            self.assertTrue(editor1.is_gt_level(editor2.level))

    def test_error_case(self):
        with self.settings(RESTCLIENTS_TRUMBA_SEA_DAO_CLASS=SEA_DAO_CLASS):
            per_m = PermissionManager()
            sea_cal = TrumbaCalendar(calendarid=100,
                                     campus='sea',
                                     name='Seattle calendar')
            self.assertRaises(DataFailureException,
                              per_m.get_permissions,
                              sea_cal)
            self.assertRaises(DataFailureException,
                              per_m.exists,
                              sea_cal)
            self.assertRaises(DataFailureException,
                              per_m.get_editor_permissions,
                              sea_cal)

    def test_set_permissions(self):
        with self.settings(RESTCLIENTS_TRUMBA_BOT_DAO_CLASS=BOT_DAO_CLASS,
                           RESTCLIENTS_TRUMBA_SEA_DAO_CLASS=SEA_DAO_CLASS,
                           RESTCLIENTS_TRUMBA_TAC_DAO_CLASS=TAC_DAO_CLASS):
            sea_cal = TrumbaCalendar(calendarid=1,
                                     campus='sea',
                                     name='Seattle calendar')
            per_m = PermissionManager()
            self.assertTrue(per_m.set_editor_permission(sea_cal, 'test10'))
            self.assertTrue(per_m.set_showon_permission(sea_cal, 'test10'))
            self.assertTrue(per_m.remove_permission(sea_cal, 'test10'))

            bot_cal = TrumbaCalendar(calendarid=2,
                                     campus='bot',
                                     name='Bothell calendar')
            per_m = PermissionManager()
            self.assertTrue(per_m.set_editor_permission(bot_cal, 'test10'))
            self.assertTrue(per_m.set_showon_permission(bot_cal, 'test10'))
            self.assertTrue(per_m.remove_permission(bot_cal, 'test10'))

            tac_cal = TrumbaCalendar(calendarid=3,
                                     campus='tac',
                                     name='Tacoma calendar')
            per_m = PermissionManager()
            self.assertTrue(per_m.set_editor_permission(tac_cal, 'test10'))
            self.assertTrue(per_m.set_showon_permission(tac_cal, 'test10'))
            self.assertTrue(per_m.remove_permission(tac_cal, 'test10'))
