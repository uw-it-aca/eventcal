from django.test import TestCase
from uw_gws.models import GroupReference
from uw_trumba.models import TrumbaCalendar
from accountsynchr.dao import DataFailureException
from accountsynchr.dao.trumba import CalPermManager, remove_permission


class TestCalPermManager(TestCase):

    def test_cal_perm_manager(self):
        cal_per_m = CalPermManager()
        self.assertTrue(cal_per_m.exists('bot'))
        self.assertTrue(cal_per_m.exists('sea'))
        self.assertTrue(cal_per_m.exists('tac'))
        self.assertEqual(cal_per_m.total_calendars('bot'), 3)
        self.assertEqual(cal_per_m.total_calendars('sea'), 2)
        self.assertEqual(cal_per_m.total_calendars('tac'), 1)

        self.assertEqual(cal_per_m.total_accounts(), 6)
        self.assertTrue(cal_per_m.account_exists('dummyp'))
        self.assertTrue(cal_per_m.account_exists('dummye'))
        self.assertTrue(cal_per_m.account_exists('dummys'))
        self.assertTrue(cal_per_m.account_exists("tdummyp"))
        self.assertTrue(cal_per_m.account_exists("tdummye"))
        self.assertTrue(cal_per_m.account_exists("tdummys"))

        sea_cal = TrumbaCalendar(calendarid=1,
                                 campus='sea',
                                 name='Seattle calendar')
        perms = cal_per_m.get_permissions(sea_cal)
        self.assertEqual(len(perms), 3)
        self.assertEqual(perms[0].to_json(),
                         {'display_name': 'publisher',
                          'level': 'PUBLISH',
                          'uwnetid': 'dummyp'})
        self.assertEqual(perms[1].to_json(),
                         {'display_name': 'editor',
                          'level': 'EDIT',
                          'uwnetid': 'dummye'})
        self.assertEqual(perms[2].to_json(),
                         {'display_name': 'showon',
                          'level': 'SHOWON',
                          'uwnetid': 'dummys'})

        self.assertTrue(cal_per_m.has_editor_permission(sea_cal, 'dummyp'))
        self.assertTrue(cal_per_m.has_editor_permission(sea_cal, 'dummye'))
        self.assertFalse(cal_per_m.has_editor_permission(sea_cal, 'dummys'))

        self.assertTrue(cal_per_m.has_showon_or_higher_permission(
                sea_cal, 'dummys'))
        self.assertTrue(cal_per_m.has_showon_or_higher_permission(
                sea_cal, 'dummyp'))
        self.assertTrue(cal_per_m.has_showon_or_higher_permission(
                sea_cal, 'dummye'))

        self.assertFalse(cal_per_m.has_showon_or_higher_permission(
                sea_cal, 'dummy'))

        not_exsit_cal = TrumbaCalendar(calendarid=101, campus='sea')
        self.assertIsNone(cal_per_m._get_perm_dict(not_exsit_cal))
        self.assertIsNone(cal_per_m.get_permission(not_exsit_cal,
                                                   'dummyp'))
        self.assertEqual(len(cal_per_m.get_permissions(not_exsit_cal)), 0)

    def test_set_permissions(self):
        cal_per_m = CalPermManager()

        self.assertTrue(cal_per_m.add_account('sdummye', 'sdummye'))
        self.assertRaises(DataFailureException, cal_per_m.add_account,
                          'u404', 'u404')

        sea_cal = TrumbaCalendar(calendarid=1, campus='sea')

        self.assertFalse(cal_per_m.has_editor_permission(sea_cal, 'sdummye'))
        self.assertTrue(cal_per_m.set_editor_permission(sea_cal, 'sdummye'))
        # print("///{0}".format(cal_per_m.get_calendar('sea', 1)))
        self.assertTrue(cal_per_m.has_editor_permission(sea_cal, 'sdummye'))
        self.assertTrue(cal_per_m.has_showon_or_higher_permission(
                sea_cal, 'sdummye'))

        self.assertTrue(cal_per_m.set_showon_permission(sea_cal, 'sdummys'))

        self.assertRaises(DataFailureException,
                          cal_per_m.set_editor_permission,
                          sea_cal, 'u404')

        self.assertTrue(remove_permission(sea_cal, 'test10'))
        self.assertRaises(DataFailureException, remove_permission,
                          sea_cal, 'u404')

        bot_cal = TrumbaCalendar(calendarid=2, campus='bot')
        self.assertTrue(cal_per_m.set_editor_permission(bot_cal, 'test10'))
        self.assertTrue(cal_per_m.has_editor_permission(bot_cal, 'test10'))

        self.assertFalse(cal_per_m.set_showon_permission(bot_cal, 'test10'))
        self.assertTrue(cal_per_m.has_editor_permission(bot_cal, 'test10'))
        self.assertTrue(remove_permission(bot_cal, 'test10'))
        self.assertTrue(cal_per_m.set_showon_permission(bot_cal, 'test11'))

        tac_cal = TrumbaCalendar(calendarid=3, campus='tac')
        self.assertTrue(remove_permission(tac_cal, 'tdummyp'))
